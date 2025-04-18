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

