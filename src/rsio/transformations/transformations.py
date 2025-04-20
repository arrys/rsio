from os import mkdir
from os.path import exists, dirname, join
from pathlib import Path

import jinja2

from rsio.metamodels.aadl2il import System
import datetime

from rsio.utils.auxiliary import get_custom_code, replace_custom_code


def _add_requirements_file(file_path: Path = Path("requirements.txt")):
    """Function to add a requirement.txt to the provided path."""
    with file_path.open("a", encoding="utf-8") as f:
        f.write(
            "robosapiensio==0.3.19\n"
            "jsonpickle==3.3.0\n"
            "paho-mqtt==2.1.0\n"
            "PyYAML==6.0.2\n"
        )


def _add_docker_file(file: str = "Dockerfile", cmp_name: str = "", path: Path | None = None):
    """Function to add a Dockerfile to the provided path."""
    path = Path(path) if path is not None else Path(".")
    dockerfile_path = path / file
    # TODO Move this to template
    content = f"""FROM python:3.10
ENV PYTHONUNBUFFERED 1

ADD . c:/src/app
WORKDIR c:/src/app
ENV PYTHONPATH c:/src/app:$PYTHONPATH

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY config.yaml ./
COPY messages.py ./
COPY . .

CMD ["python3", "{cmp_name}.py"]

"""
    dockerfile_path.write_text(content)


def swc2code_py(system: System | None = None, path: Path = Path("output/generated")):
    """
    Generate Python code from the system modeled within the AADL Intermediate Language (AADLIL).

    :param system: Adaptive system model within AADLIL, defaults to None
    :param path: Output directory for the generated code, defaults to "output/generated"
    """
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine.
    this_folder = Path(__file__).resolve().parent
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load templates
    template = jinja_env.get_template("templates/swc_py.template")
    template_config = jinja_env.get_template("templates/swc_config.template")
    template_messages = jinja_env.get_template("templates/messages_py.template")

    managing_system = system.systems[0]
    for process in managing_system.processes:
        swc_folder = path / process.name
        swc_folder.mkdir(parents=True, exist_ok=True)

        swc_file_path = swc_folder / f"{process.name}.py"
        swc_exists = swc_file_path.is_file()

        if swc_exists:
            content = swc_file_path.read_text()
            cc_include = get_custom_code(text=content, tag="include")
            cc_code = get_custom_code(text=content, tag="code")
            cc_init = get_custom_code(text=content, tag="init")
            cc_thread_code = [
                get_custom_code(text=content, tag=f"code_{thread.name}")
                for thread in process.threads
            ]

        # Generate new SWC file
        swc_file_path.write_text(template.render(swc=process))

        # If SWC existed, restore custom code
        if swc_exists:
            content = swc_file_path.read_text()
            content = replace_custom_code(content, tag="include", replacement=cc_include)
            content = replace_custom_code(content, tag="code", replacement=cc_code)
            content = replace_custom_code(content, tag="init", replacement=cc_init)
            for i, thread in enumerate(process.threads):
                content = replace_custom_code(content, tag=f"code_{thread.name}", replacement=cc_thread_code[i])
            swc_file_path.write_text(content)

        # Generate config.yaml
        ip = "localhost"
        for processor in managing_system.processors:
            if processor.runs_rap_backbone:
                ip = processor.ip
        (swc_folder / "config.yaml").write_text(template_config.render(swc=process, IP=ip))

        # Generate messages.py
        (swc_folder / "messages.py").write_text(template_messages.render(messages=system.messages))

        # Add requirements.txt and Dockerfile if not present before
        if not swc_exists:
            _add_requirements_file(path=swc_folder)
            _add_docker_file(cmp_name=process.name, path=swc_folder)


def message2code_py(system: System | None = None, path: Path = Path("output/generated/messages")):
    """
    Generate Python code from messages modeled within the AADL Intermediate Language (AADLIL).

    :param system: Adaptive system model within AADLIL, defaults to None
    :param path: Output directory for the generated code, defaults to "output/generated/messages"
    """
    # Ensure output directory exists
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine
    this_folder = Path(__file__).resolve().parent
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template("templates/messages_py.template")

    # Write the rendered template
    output_file = path / "messages.py"
    output_file.write_text(template.render(messages=system.messages))


def swc2launch(system: System | None = None, path: Path = Path("output/generated/launch")):
    """
    Generate launch files for the given system deployment.

    :param system: Managing or managed system model within AADLIL, defaults to None
    :param path: Output directory for the generated launch files, defaults to "output/generated/launch"
    """
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine.
    this_folder = Path(__file__).resolve().parent
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template("templates/swc_launch.template")

    # Extract all processors of the managing system
    for processor in system.processors:
        processor_path = path / processor.name
        processor_path.mkdir(parents=True, exist_ok=True)

        launch_file = processor_path / "launch.xml"
        launch_file.write_text(template.render(processor=processor))


def swc2main(system: System | None = None, package: str = "", prefix = None, path: Path = Path("output/generated/main")):
    """
    Generate main files for the given system deployment.

    :param system: Managing or managed system model within AADLIL, defaults to None
    :param package: Package name, defaults to an empty string
    :param path: Output directory for the generated main files, defaults to "output/generated/main"
    """
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine.
    this_folder = Path(__file__).parent
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template("templates/swc_launch_main.template")

    # Extract all processors of the managing system
    for processor in system.processors:
        main_file = path / f"main_{processor.name}.py"
        with main_file.open("w") as f:
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
    template = jinja_env.get_template("templates/aadl_messages.template")

    # Extract all processes from AADL system model
    with open(join(path, "messages.aadl"), "w") as f:
        f.write(template.render(types=maplek.types))


def robochart2logical(parsed, path: Path=Path("output/generated/LogicalArchitecture")):
    """
    Generate AADL logical architecture from RoboChart models.

    :param path: Path to the output folder, defaults to "output/generated/messages"
    """
    path.mkdir(parents=True, exist_ok=True)


    # Initialize the Templates engine.
    this_folder = Path(__file__).parent
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template("templates/aadl_logical.template")

    # Prepare the parsed models for code generation
    elements = [parsed.monitor_model, parsed.analysis_model, parsed.plan_model, parsed.legitimate_model,
                parsed.execute_model, parsed.knowledge_model]

    # Extract all processes from AADL system model
    (path / "LogicalArchitecture.aadl").write_text(template.render(elements=elements))


def swc2docker_compose(system: System | None = None, path: Path = Path("output/generated/docker")):
    """
    Generate Docker Compose for the given system deployment.

    :param system: Managing or managed system model within AADLIL, either managing or managed system, defaults to None
    :type system: object, optional
    :param path: Path to the output directory, defaults to "output/generated/launch"
    :type path: str, optional
    """
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine.
    this_folder = Path(__file__).parent
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template("templates/swc_docker_compose.template")

    # Extract all processors of the managing system
    for processor in system.processors:
        processor_path = path / processor.name
        processor_path.mkdir(parents=True, exist_ok=True)
        compose_file = processor_path / "compose.yaml"
        compose_file.write_text(template.render(processor=processor))


def update_robosapiens_io_ini(system: System | None = None, package: str = "", prefix: str = "", path: Path = Path.cwd()):
    """Update the RoboSapiensIO configuration."""
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine
    this_folder = Path(__file__).parent
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Load the template
    template = jinja_env.get_template("templates/robosapiensIO_ini.template")

    formatted_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Write to .ini file
    (path / "robosapiensIO.ini").write_text(
        template.render(
            system=system,
            package=package,
            prefix=prefix,
            timestamp=formatted_timestamp,
            managingSystem=system.systems[0],
            managedSystem=system.systems[1]
        )
    )


def add_backbone_config(system: System | None = None, path : Path = Path.cwd()):
    """
    Add the RoboSAPIENS Adaptive Platform backbone configuration to the repository.

    :param system: Managing or managed system model within AADLIL, either managing or managed system, defaults to None
    :param path: Path to the robosapiensIO.ini file, defaults to "Resources"
    """
    path.mkdir(parents=True, exist_ok=True)

    # Initialize the Templates engine
    this_folder = Path(__file__).parent
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Load the templates
    template_mqtt = jinja_env.get_template("templates/mqtt_config.template")
    template_redis = jinja_env.get_template("templates/redis_config.template")

    # Write configuration files
    (path / "acl.conf").write_text(template_mqtt.render(system=system))
    (path / "redis.conf").write_text(template_redis.render(system=system))
