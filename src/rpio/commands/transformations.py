import logging
from pathlib import Path

import click

from rpio.metamodels.aadl2il import System
from rpio.parsers.parsers import AadlParser
from rpio.transformations.transformations import message2code_py, swc2code_py, swc2launch, swc2main, swc2docker_compose, \
    add_backbone_config, update_robosapiens_io_ini


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

    # TODO Should any of these errors force an exit?
    if aadl2aadlil:
        logger.debug("WARNING: AADL2AADLIL transformation is under development.")

        # 1. Setup the AADL parser
        try:
            parser = AadlParser(
                logical_architecture=Path("Design/logicalArchitecture.aadl"),
                physical_architecture=Path("Design/physicalArchitecture.aadl"),
                messages=Path("Design/messages.aadl")
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
            s.object2json(Path("Design/design.json"))
        except:
            logger.error("ERROR: AADLIL model could not be generated.")

    if aadlil2code:
        logger.warning("WARNING: AADLIL2CODE transformation is under development.")

        # 1. LOAD THE AADL INTERMEDIATE LANGUAGE
        try:
            design = System(name="adaptiveSystem", description="Design generated from the AADLIL file", json_descriptor=Path("Design/design.json"))
        except:
            design = None
            logger.error("ERROR: The AADIL file could not be loaded, please check if it exists (Design/design.json).")

        # 2. GENERATE CUSTOM MESSAGES FROM AADL INTERMEDIATE LANGUAGE
        try:
            message2code_py(design, Path("Realization/ManagingSystem/Messages"))
            message2code_py(design, Path("Realization/ManagedSystem/Messages"))
        except:
            logger.error("ERROR: Messages could not be generated, no design loaded.")

        # 3. GENERATE SWC CODE FROM AADL INTERMEDIATE LANGUAGE
        try:
            swc2code_py(design, Path("Realization/ManagingSystem/Nodes"))
        except:
            logger.error("ERROR: Code could not be generated, no design loaded.")

        # 3. GENERATE PLATFORM LAUNCH FILES
        try:
            swc2launch(design.systems[0], Path("Realization/ManagingSystem/Platform"))
            swc2launch(design.systems[1], Path("Realization/ManagedSystem/Platform"))
        except:
            logger.error("ERROR: Platform-specific launch file could not be generated, no design loaded.")

        # 3. GENERATE PLATFORM MAIN FILES
        try:
            current_folder_name = Path.cwd().name
            swc2main(system=design.systems[0], package=current_folder_name, prefix=None, path=Path("Resources"))
        except:
            logger.error("ERROR: Platform(s) main file could not be generated.")

        # 4. GENERATE PLATFORM DOCKER COMPOSE
        try:
            swc2docker_compose(system=design.systems[0], path=Path("Realization/ManagingSystem/Platform"))
            add_backbone_config(system=design, path=Path("Resources"))
        except:
            logger.error("ERROR: Platform(s) docker compose file could not be generated.")

        # 8. update the roboSapiensIO.ini file based on the generation
        try:
            update_robosapiens_io_ini(system=design)
        except:
            logger.error("ERROR: robosapiensIO.ini file could not be updated.")
