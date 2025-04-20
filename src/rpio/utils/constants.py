import platform
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from typing import TypeVar, Type


class OrchestrationType:
    FMI_local = "FMI_LOCAL"
    DISTRIBUTED = "DISTRIBUTED"
    DISTRIBUTED_FIXED_IO = "DISTRIBUTED_FIXED_IO"

class ExecutionPatterns:
    TRIGGERED = "TRIGGERED"
    IPO = "IPO"
    IOP = "IOP"

class VerificationMethods:
    STATICLOWERBOUND = "StaticLowerBound"
    STATICUPPERBOUND = "StaticUpperBound"
    STATICBOUND = "StaticBound"

class MonitorType:
    RUNTIME = "runtime"
    POSTPROCESSING = "postprocessing"

class StepStatus:
    PENDING = "Pending"
    RUNNING = "Running"
    PASSED = "Passed"
    FAILED = "Failed"

@dataclass
class ProjectDirectories: # TODO Make into two classes with one handling the templated stuff
    name: str
    deploy_file_path: Path = Path("Realization/ManagingSystem/Actions/deploy.py")
    build_file_path: Path = Path("Realization/ManagingSystem/Actions/build.py")
    run_file_path: Path = Path("Realization/ManagingSystem/Actions/run.py")

    platform_config_template: str = "Realization/ManagingSystem/Platform/{name}/config.yaml"
    launch_xml_file_path_template: str = "Realization/ManagingSystem/Platform/{name}/launch.xml"

    @property
    def platform_config(self) -> Path:
        return Path(self.platform_config_template.format(name=self.name))

    # def create_paths(self) -> None:
    #     for path in (self.run_file, self.output_data):
    #         path.mkdir(parents=True, exist_ok=True)

RS_STRUCTURE = ProjectDirectories("package")

VIRTUAL_ENVIRONMENT_NAME = "rpiovenv"


class Formalism(Enum):
    PYTHON = "Python"
    CPP = "C++"
    JAVA = "Java"
    CSHARP = "C#"
    JAVASCRIPT = "JavaScript"
    RUST = "Rust"
    GO = "Go"
    KOTLIN = "Kotlin"


class Deployment(Enum):
    VIRTUAL = "virtualenv"
    NATIVE = "native"
    CONTAINER = "containerized"


EnumType = TypeVar("EnumType", bound=Enum)


def enum_from_name(name: str, enum: Type[EnumType]) -> EnumType:
    """Convert a case-insensitive name to an EnumType."""
    for member in enum:
        if member.value.lower() == name.lower():
            return member
    raise ValueError(f"Unknown {enum.__name__}: {name}")


def formalism_from_name(name: str) -> Formalism:
    """Convert a case-insensitive name to a Formalism."""
    return enum_from_name(name, Formalism)


def deployment_from_name(name: str) -> Deployment:
    """Convert a case-insensitive name to a Deployment."""
    return enum_from_name(name, Deployment)

class OperatingSystem(Enum):
    WINDOWS = "windows"
    UNIX = "unix"


def detect_operating_system() -> OperatingSystem:
    system = platform.system()
    if system == "Windows":
        return OperatingSystem.WINDOWS
    elif system in {"Linux", "Darwin"}:
        return OperatingSystem.UNIX
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")
