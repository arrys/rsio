import logging
import click

from rpio.metamodels.aadl2_IL import System
from rpio.parsers.parsers import AADL_parser
from rpio.transformations.transformations import message2code_py, swc2code_py, swc2launch, swc2main, swc2docker_compose, \
    add_backbone_config, update_robosapiens_io_ini


# from rpio.transformations.transformations import *
# from rpio.parsers.parsers import *
# from rpio.metamodels.aadl2_IL import *


@click.group()
@click.pass_context
def transformation_cmds():
    pass


@transformation_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--roboarch2aadl", is_flag=True, default=False, help="Perform the roboArch2AADL transformation.")
@click.option("--aadl2aadlil", is_flag=True, default=False, help="Perform the AADL2AADLIL transformation.")
@click.option("--aadlil2code", is_flag=True, default=False, help="Perform the AADLIL2CODE transformation.")
def transformation(verbose: bool, roboarch2aadl: bool, aadl2aadlil: bool, aadlil2code: bool):
    """Performing one of the model-to-model or model-to-code transformations."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)

    if roboarch2aadl:
        logger.debug("WARNING: RoboArch2AADL transformation is not implemented yet.")

    if aadl2aadlil:
        logger.debug("WARNING: AADL2AADLIL transformation is under development.")

        # 1. Setup the AADL parser
        try:
            parser = AADL_parser(
                logical_architecture="Design/logicalArchitecture.aadl",
                physical_architecture="Design/physicalArchitecture.aadl",
                messages="Design/messages.aadl"
            )
        except:
            parser = None
            logger.error("ERROR: AADL parser could not be instantiated, check if AADL models are available (Design/*.aadl).")

        # 2. parse the aadl models and store in AADLIL
        try:
            s = parser.aadl2aadl_il()
        except:
            s = None
            logger.error("ERROR: AADL parsing failed, check if AADL models are available (Design/*.aadl).")

        # 3. dump to aadlil json
        try:
            s.object2json(fileName="Design/design.json")
        except:
            logger.error("ERROR: AADLIL model could not be generated.")

    if aadlil2code:
        logger.warning("WARNING: AADLIL2CODE transformation is under development.")

        # 1. LOAD THE AADL INTERMEDIATE LANGUAGE
        try:
            design = System(name="adaptiveSystem", description="Design generated from the AADLIL file", json_descriptor="Design/design.json")
        except:
            design = None
            logger.error("ERROR: The AADIL file could not be loaded, please check if it exists (Design/design.json).")

        # 2. GENERATE CUSTOM MESSAGES FROM AADL INTERMEDIATE LANGUAGE
        try:
            message2code_py(system=design, path="Realization/ManagingSystem/Messages")
            message2code_py(system=design, path="Realization/ManagedSystem/Messages")
        except:
            logger.error("ERROR: Messages could not be generated, no design loaded.")

        # 3. GENERATE SWC CODE FROM AADL INTERMEDIATE LANGUAGE
        try:
            swc2code_py(system=design, path="Realization/ManagingSystem/Nodes")
        except:
            logger.error("ERROR: Code could not be generated, no design loaded.")

        # 3. GENERATE PLATFORM LAUNCH FILES
        try:
            swc2launch(system=design.systems[0], path="Realization/ManagingSystem/Platform")
            swc2launch(system=design.systems[1], path="Realization/ManagedSystem/Platform")
        except:
            logger.error("ERROR: Platform-specific launch file could not be generated, no design loaded.")

        # 3. GENERATE PLATFORM MAIN FILES
        try:
            current_folder_path, current_folder_name = os.path.split(os.getcwd())
            swc2main(system=design.systems[0], package=current_folder_name, prefix=None, path="Resources")
        except:
            logger.error("ERROR: Platform(s) main file could not be generated.")

        # 4. GENERATE PLATFORM DOCKER COMPOSE
        try:
            swc2docker_compose(system=design.systems[0], path="Realization/ManagingSystem/Platform")
            add_backbone_config(system=design, path="Resources")
        except:
            logger.error("ERROR: Platform(s) docker compose file could not be generated.")

        # 8. update the roboSapiensIO.ini file based on the generation
        try:
            update_robosapiens_io_ini(system=design, path=None)
        except:
            logger.error("ERROR: robosapiensIO.ini file could not be updated.")
