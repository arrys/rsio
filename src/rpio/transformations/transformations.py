from os import mkdir
from os.path import exists, dirname, join, isfile
import jinja2
from rpio.utils.auxiliary import *
import datetime


def _add_requirements_file(file="requirements.txt", path=None):
    """Function to add a requirement.txt to the provided path."""
    f = open(path + "/" + file, "a")
    f.write("robosapiensio==0.3.19\n")
    f.write("jsonpickle==3.3.0\n")
    f.write("paho-mqtt==2.1.0\n")
    f.write("PyYAML==6.0.2\n")
    f.close()


def _add_docker_file(file="Dockerfile", cmp_name="", path=None):
    """Function to add a requirement.txt to the provided path."""

    f = open(path + "/" + file, "a")

    # --- custom file content ---
    f.write("FROM python:3.10\n")
    f.write("ENV PYTHONUNBUFFERED 1\n")
    f.write("\n")
    f.write("ADD . c:/src/app\n")
    f.write("WORKDIR c:/src/app\n")
    f.write("ENV PYTHONPATH c:/src/app:$PYTHONPATH\n")
    f.write("\n")
    f.write("COPY requirements.txt ./\n")
    f.write("RUN pip3 install --no-cache-dir -r requirements.txt\n")
    f.write("\n")
    f.write("COPY config.yaml ./\n")
    f.write("COPY messages.py ./\n")
    f.write("COPY . .\n")
    f.write("\n")
    f.write('CMD ["python3", "' + cmp_name + '.py"]\n')
    f.write("\n")

    f.close()


def swc2code_py(system=None, path="output/generated"):
    """
    Generate Python code from the system modeled within the AADL Intermediate Language (AADLIL).

    :param system: Adaptive system model within AADLIL, defaults to None
    :type system: object, optional
    :param path: Output directory for the generated code, defaults to "output/generated/messages"
    :type path: str, optional
    :return: None
    :rtype: None
    """

    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/swc_py.template')
    template_config = jinja_env.get_template('templates/swc_config.template')
    template_messages = jinja_env.get_template('templates/messages_py.template')

    # Extract all processes from AADL system model
    managing_system = system.systems[0]
    for process in managing_system.processes:

        # 0. Generate folder for each AADL process
        swc_folder = path + "/" + process.name
        if not exists(swc_folder):
            mkdir(swc_folder)

        # 1. Check if SWC file exists
        swc_exists = isfile(join(swc_folder, process.name + ".py"))

        # 2. If swc exists, store custom code added by the user
        if swc_exists:
            with open(join(swc_folder, process.name + ".py"), "r") as swc_file:
                content = swc_file.read()
                cc_include = get_custom_code(text=content, tag="include")
                cc_code = get_custom_code(text=content, tag="code")
                cc_init = get_custom_code(text=content, tag="init")
                cc_thread_code = []
                for thread in process.threads:
                    _cc_code = get_custom_code(text=content, tag="code_" + thread.name)
                    cc_thread_code.append(_cc_code)

        # 2. Generate code from AADL processes
        with open(join(swc_folder, process.name + ".py"), 'w') as f:
            f.write(template.render(swc=process))

        # 3. If swc exists, replace custom code in generated template
        if swc_exists:
            with open(join(swc_folder, process.name + ".py"), "r") as swc_file:
                content = swc_file.read()
                content = replace_custom_code(content, tag="include", replacement=cc_include)
                content = replace_custom_code(content, tag="code", replacement=cc_code)
                content = replace_custom_code(content, tag="init", replacement=cc_init)
                for i in range(0, len(process.threads), 1):
                    content = replace_custom_code(content, tag="code_" + process.threads[i].name, replacement=cc_thread_code[i])

            with open(join(swc_folder, process.name + ".py"), "w") as swc_file:
                swc_file.write(content)

        # 4. Generate config.yaml file from AADL processes

        # determine the IP address of the platform running the process
        _ip = "localhost"
        for processor in managing_system.processors:
            if processor.runs_rap_backbone:
                _ip = processor.ip

        with open(join(swc_folder, "config.yaml"), 'w') as f:
            f.write(template_config.render(swc=process, IP=_ip))

        # 5. Generate messages for standalone components
        with open(join(swc_folder, "messages.py"), 'w') as f:
            f.write(template_messages.render(messages=system.messages))

        # 6. Add requirements.txt if swc does not exist
        if not swc_exists:
            _add_requirements_file(path=swc_folder)

        # 7. Add Docker file if swc does not exist
        if not swc_exists:
            _add_docker_file(cmp_name=process.name, path=swc_folder)


def message2code_py(system=None, path="output/generated/messages"):
    """
    Generate Python code from messages modeled within the AADL Intermediate Language (AADLIL).

    :param system: Adaptive system model within AADLIL, defaults to None
    :type system: object, optional
    :param path: Output directory for the generated code, defaults to "output/generated/messages"
    :type path: str, optional
    :return: None
    :rtype: None
    """

    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/messages_py.template')

    # Extract all processes from AADL system model
    with open(join(path, "messages.py"), 'w') as f:
        f.write(template.render(messages=system.messages))


def swc2launch(system=None, path="output/generated/launch"):
    """
    Generate launch files for the given system deployment.

    :param system: Managing or managed system model within AADLIL, defaults to None
    :type system: object, optional
    :param path: Output directory for the generated launch files, defaults to "output/generated/launch"
    :type path: str, optional
    :return: None
    :rtype: None
    """
    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/swc_launch.template')

    # Extract all processors of the managing system
    for processor in system.processors:
        processor_path = join(path, processor.name)
        if not exists(processor_path):
            mkdir(processor_path)

        with open(join(processor_path, "launch.xml"), 'w') as f:
            f.write(template.render(processor=processor))


def swc2main(system=None, package="", prefix=None, path="output/generated/main"):
    """
    Generate main files for the given system deployment.

    :param system: Managing or managed system model within AADLIL, defaults to None
    :type system: object, optional
    :param package: Package name, defaults to an empty string
    :type package: str, optional
    :param path: Output directory for the generated main files, defaults to "output/generated/launch"
    :type path: str, optional
    :return: None
    :rtype: None
    """
    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/swc_launch_main.template')

    # Extract all processors of the managing system
    for processor in system.processors:
        with open(join(path, "main_" + processor.name + ".py"), 'w') as f:
            f.write(template.render(processor=processor, package=package, prefix=prefix))


def robochart2aadlmessages(maplek=None, path="output/generated/messages"):
    """
    Generate AADL messages from RoboChart models.

    :param MAPLEK: MAPLE-K modeled within RoboChart, defaults to None
    :type MAPLEK: object, optional
    :param path: Path to the output folder, defaults to "output/generated/messages"
    :type path: str, optional
    :return: None
    :rtype: None
    """

    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/aadl_messages.template')

    # Extract all processes from AADL system model
    with open(join(path, "messages.aadl"), 'w') as f:
        f.write(template.render(types=maplek.types))


def robochart2logical(parsed=None, path="output/generated/LogicalArchitecture"):
    """
    Generate AADL logical architecture from RoboChart models.

    :param path: Path to the output folder, defaults to "output/generated/messages"
    :type path: str, optional
    :return: None
    :rtype: None
    """

    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/aadl_logical.template')

    # Prepare the parsed models for code generation
    elements = [parsed.monitor_model, parsed.analysis_model, parsed.plan_model, parsed.legitimate_model,
                parsed.execute_model, parsed.knowledge_model]

    # Extract all processes from AADL system model
    with open(join(path, "LogicalArchitecture.aadl"), 'w') as f:
        f.write(template.render(elements=elements))


def swc2docker_compose(system=None, path="output/generated/docker"):
    """
    Generate Docker Compose for the given system deployment.

    :param system: Managing or managed system model within AADLIL, either managing or managed system, defaults to None
    :type system: object, optional
    :param path: Path to the output directory, defaults to "output/generated/launch"
    :type path: str, optional
    :return: None
    :rtype: None
    """
    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/swc_docker_compose.template')

    # Extract all processors of the managing system
    for processor in system.processors:

        processor_path = join(path, processor.name)
        if not exists(processor_path):
            mkdir(processor_path)

        with open(join(processor_path, "compose.yaml"), 'w') as f:
            f.write(template.render(processor=processor))


def update_robosapiens_io_ini(system=None, package="", prefix="", path="output/generated/docker"):
    """
    Update the RoboSapiensIO configuration.

    :param system: Managing or managed system model within AADLIL, either managing or managed system, defaults to None
    :type system: object, optional
    :param path: Path to the robosapiensIO.ini file, defaults to "output/generated/launch"
    :type path: str, optional
    :return: None
    :rtype: None
    """
    if path is None:
        path = os.getcwd()
    else:
        if not exists(path):
            mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/robosapiensIO_ini.template')

    current_timestamp = datetime.datetime.now()
    formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    managing_system = system.systems[0]
    managed_system = system.systems[1]

    with open(join(path, "robosapiensIO.ini"), 'w') as f:
        f.write(template.render(system=system, package=package, prefix=prefix, timestamp=formatted_timestamp.__str__(),
                                managingSystem=managing_system, managedSystem=managed_system))


def add_backbone_config(system=None, path='Resources'):
    """
    Add the RoboSAPIENS Adaptive Platform backbone configuration to the repository.

    :param system: Managing or managed system model within AADLIL, either managing or managed system, defaults to None
    :type system: object, optional
    :param path: Path to the robosapiensIO.ini file, defaults to "Resources"
    :type path: str, optional
    :return: None
    :rtype: None
    """

    if path is None:
        path = os.getcwd()
    else:
        if not exists(path):
            mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the templates
    template_mqtt = jinja_env.get_template('templates/mqtt_config.template')
    template_redis = jinja_env.get_template('templates/redis_config.template')

    with open(join(path, "acl.conf"), 'w') as f:
        f.write(template_mqtt.render(system=system))

    with open(join(path, "redis.conf"), 'w') as f:
        f.write(template_redis.render(system=system))
