# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.workflow.tasks import *
from rpio.workflow.executer import Executer_GUI


# 1 . define the tasks
tasks = {
    "Generate AADL messages": t_robochart_to_messages,
    "Generate AADL Logical Architecture": t_robochart_to_logical
}

# 2. Launch the graphical executer
app = Executer_GUI(tasks=tasks,name="ROBOCHART2AADL")
app.root.mainloop()
