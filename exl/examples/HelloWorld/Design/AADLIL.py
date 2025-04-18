from rpio.metamodels.aadl2_IL import *



def HelloWorld():
    #-----------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------- MESSAGES ----------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------


    #laserScan message
    ranges = Data(name='ranges', data_type="Array")
    angle_increment = Data(name='angle_increment', data_type="Float_64")

    laser_scan = Message(name="LaserScan", feature_list=[ranges, angle_increment])

    # rotationAction message
    omega = Data(name="omega", data_type="Float_64")
    duration = Data(name="duration", data_type="Float_64")
    direction = Message(name="Direction", feature_list=[omega, duration])

    # new_data message
    new_data = Data(name="new_data", data_type="Boolean")
    new_data_message = Message(name="NewData", feature_list=[new_data])
    # anomaly message
    anomaly = Data(name="anomaly", data_type="Boolean")
    anomaly_message = Message(name="AnomalyMessage", feature_list=[anomaly])

    new_plan = Data(name="NewPlan", data_type="Boolean")
    new_plan_message = Message(name="NewPlanMessage", feature_list=[new_plan])

    # legitimate message
    legitimate = Data(name="legitimate", data_type="Boolean")
    legitimate_message = Message(name="LegitimateMessage", feature_list=[legitimate])

    #-----------------------------------------------------------------------------------------------------------------------
    #--------------------------------------- LOGICAL ARCHITECTURE ----------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------
    adaptiveSystem = System(name="adaptiveSystem", description="Example adaptive system", message_list=[laser_scan, direction, anomaly_message, new_plan_message])

    #-A- --- managed system ---
    managedSystem = System(name="managedSystem", description="managed system part")

    _laserScan_OUT = OutPort(name="laser_scan", type="event data", message= laser_scan)
    _direction_IN = InPort(name="direction", type="event data", message=direction)

    managedSystem.add_feature(_laserScan_OUT)
    managedSystem.add_feature(_direction_IN)

    #-B- --- managing system ---

    managingSystem = System(name="managingSystem", description="managing system part")

    _laser_scan_IN = InPort(name="laser_scan", type="event data", message=laser_scan)
    _direction_OUT = OutPort(name="direction", type="event data", message=direction)

    managingSystem.add_feature(_laser_scan_IN)
    managingSystem.add_feature(_direction_OUT)

    # connections
    c1 = Connection(source=_laserScan_OUT, destination=_laser_scan_IN)
    c2 = Connection(source=_direction_OUT, destination=_direction_IN)


    #---------------------COMPONENT LEVEL---------------------------

    #-MONITOR-
    monitor = Process(name="Monitor", description="monitor component")

    _laserScan = OutPort(name="laser_scan", type="data", message=laser_scan)
    _new_data_out = OutPort(name="new_data", type="event", message=new_data_message)


    monitor.add_feature(_laserScan)
    monitor.add_feature(_new_data_out)

    monitor_data = Thread(name="monitor_data", feature_list=[_laserScan, _new_data_out], event_trigger='Scan')
    monitor.add_thread(monitor_data)

    #-ANALYSIS-
    analysis = Process(name="Analysis", description="analysis component")

    _laserScan_in = InPort(name="laser_scan", type="data", message=laser_scan)
    _anomaly_out = OutPort(name="anomaly", type="event", message=anomaly_message)

    analysis.add_feature(_laserScan_in)
    analysis.add_feature(_anomaly_out)

    analyse_scan_data = Thread(name="analyse_scan_data", feature_list=[_laserScan_in, _anomaly_out], event_trigger='new_data')
    analysis.add_thread(analyse_scan_data)


    #-PLAN-
    plan = Process(name="Plan", description="plan component")

    #TODO: define input
    _anomaly_in = InPort(name="anomaly", type="event", message=anomaly_message)
    _plan_out = OutPort(name="new_plan", type="data", message=new_plan_message)
    _diraction_out = OutPort(name="direction", type="data", message=direction)

    plan.add_feature(_anomaly_in)
    plan.add_feature(_plan_out)
    plan.add_feature(_diraction_out)

    planner = Thread(name="planner", feature_list=[_anomaly_in, _plan_out, _diraction_out], event_trigger='anomaly')
    plan.add_thread(planner)

    #-LEGITIMATE-
    legitimate = Process(name="Legitimate", description="legitimate component")

    #-EXECUTE-
    execute = Process(name="Execute", description="execute component")

    _new_plan_in = InPort(name="new_plan", type="event", message=direction)
    _isLegit = InPort(name="isLegit", type="event data", message=legitimate_message)
    _directions = InPort(name="directions", type="data", message=direction)
    _directions_out = OutPort(name="spin_config", type="data event", message=direction)

    execute.add_feature(_new_plan_in)
    execute.add_feature(_isLegit)
    execute.add_feature(_directions)
    execute.add_feature(_directions_out)

    executer = Thread(name="executer", feature_list=[_new_plan_in, _isLegit, _directions, _directions_out])
    execute.add_thread(executer)

    # #-KNOWLEDGE-
    # knowledge = process(name="knowledge", description="knowledge component")
    #
    # _weatherConditions = port(name="weatherConditions",type="event data", message=weatherConditions)
    # _shipPose = port(name="shipPose",type="event data", message=shipPose)
    # _shipAction = port(name="shipAction",type="event data", message=shipAction)
    # _pathEstimate = port(name="pathEstimate",type="event data", message=predictedPath)
    # _pathAnomaly = port(name="pathAnomaly",type="event data", message=AnomalyMessage)
    # _plan = port(name="plan",type="event data", message=predictedPath)
    # _isLegit = port(name="isLegit",type="event data", message=legitimateMessage)

    # knowledge.addFeature(_weatherConditions)
    # knowledge.addFeature(_shipPose)
    # knowledge.addFeature(_shipAction)
    # knowledge.addFeature(_pathEstimate)
    # knowledge.addFeature(_pathAnomaly)
    # knowledge.addFeature(_plan)
    # knowledge.addFeature(_isLegit)

    managingSystem.add_process(monitor)
    managingSystem.add_process(analysis)
    managingSystem.add_process(plan)
    managingSystem.add_process(legitimate)
    managingSystem.add_process(execute)
    # managingSystem.addProcess(knowledge)

    #---------------------SYSTEM LEVEL---------------------------
    adaptiveSystem.add_system(managingSystem)
    adaptiveSystem.add_system(managedSystem)


    #-----------------------------------------------------------------------------------------------------------------------
    #--------------------------------------- PHYSICAL ARCHITECTURE ---------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------

    # XEON PROCESSOR CONNTECTION
    MIPSCapacity = Characteristic(name="MIPSCapacity", value=1000.0, data_type="MIPS")
    I1 = Port(name="I1", type="event data")
    laptop_xeon1 = Processor(name="xeon1", property_list=[MIPSCapacity], feature_list=[I1], ip="192.168.56.1")
    laptop_xeon1.runs_rap_backbone= True    #RUNS THE RoboSAPIENS Adaptive Platform backbone


    # XEON PROCESSOR CONNTECTION
    MIPSCapacity = Characteristic(name="MIPSCapacity", value=2000.0, data_type="MIPS")
    I2 = Port(name="I2", type="event data")
    RPI = Processor(name="Raspberry Pi 4B", property_list=[MIPSCapacity], feature_list=[I2], ip="192.168.56.5")

    # WIFI CONNTECTION
    BandWidthCapacity = Characteristic(name="BandWidthCapacity", value=100.0, data_type="Mbytesps")
    Protocol = Characteristic(name="Protocol", value="MQTT", data_type="-")
    DataRate = Characteristic(name="DataRate", value=100.0, data_type="Mbytesps")
    WriteLatency = Characteristic(name="WriteLatency", value=4, data_type="Ms")
    interface = Bus(name="interface", property_list=[BandWidthCapacity, Protocol, DataRate, WriteLatency])

    interface.add_connection(I1)
    interface.add_connection(I2)

    #-----------------------------------------------------------------------------------------------------------------------
    #--------------------------------------- MAPPING ARCHITECTURE ----------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------

    laptop_xeon1.add_processor_binding(process=monitor)
    laptop_xeon1.add_processor_binding(process=analysis)
    laptop_xeon1.add_processor_binding(process=plan)
    #laptop_xeon1.addProcessorBinding(process=legitimate)
    laptop_xeon1.add_processor_binding(process=execute)

    managingSystem.add_processor(laptop_xeon1)
    #managingSystem.addProcessor(laptop_xeon2)
    managedSystem.add_processor(RPI)

    # -----------------------------------------------------------------------------------------------------------------------
    # --------------------------------------- NODE IMPLEMENTATION ----------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------
    monitor.formalism = "python"
    analysis.formalism = "python"
    plan.formalism = "python"
    legitimate.formalism = "python"
    execute.formalism = "python"

    monitor.containerization = True
    analysis.containerization = True
    plan.containerization = True
    legitimate.containerization = True
    execute.containerization = True


    return adaptiveSystem

HelloWorldDesign=HelloWorld()
HelloWorldDesign.object2json(file_name="design.json")


