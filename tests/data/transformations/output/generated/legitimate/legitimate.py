# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.clientLibraries.rpclpy.node import Node
from ...Messages.messages import *


class legitimate(Node):

    def __init__(self, config='config.yaml',verbose=False):
        super().__init__(config=config,verbose=verbose)

        self._name = "legitimate"
        self.logger.log("legitimate instantiated")




def main(args=None):

    node = legitimate()
    node.start()

if __name__ == '__main__':
    main()