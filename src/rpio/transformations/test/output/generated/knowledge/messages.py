class weatherConditions(object):
    def __init__(self):

        self.name= "weatherConditions"
        self._windDirection= 0.0
        self._windSpeed= 0.0


    @property
    def windDirection(self):
        """The windDirection (read-only)."""
        return self._windDirection

    @windDirection.setter
    def windDirection(self, cmp):
        """The windDirection (write)."""
        self._windDirection = cmp

    @property
    def windSpeed(self):
        """The windSpeed (read-only)."""
        return self._windSpeed

    @windSpeed.setter
    def windSpeed(self, cmp):
        """The windSpeed (write)."""
        self._windSpeed = cmp


class shipPose(object):
    def __init__(self):

        self.name= "shipPose"
        self._SurgeSpeed= 0.0
        self._SwaySpeed= 0.0
        self._YawRate= 0.0
        self._RollAngle= 0.0
        self._RollRate= 0.0
        self._Heading= 0.0
        self._x= 0.0
        self._y= 0.0


    @property
    def SurgeSpeed(self):
        """The SurgeSpeed (read-only)."""
        return self._SurgeSpeed

    @SurgeSpeed.setter
    def SurgeSpeed(self, cmp):
        """The SurgeSpeed (write)."""
        self._SurgeSpeed = cmp

    @property
    def SwaySpeed(self):
        """The SwaySpeed (read-only)."""
        return self._SwaySpeed

    @SwaySpeed.setter
    def SwaySpeed(self, cmp):
        """The SwaySpeed (write)."""
        self._SwaySpeed = cmp

    @property
    def YawRate(self):
        """The YawRate (read-only)."""
        return self._YawRate

    @YawRate.setter
    def YawRate(self, cmp):
        """The YawRate (write)."""
        self._YawRate = cmp

    @property
    def RollAngle(self):
        """The RollAngle (read-only)."""
        return self._RollAngle

    @RollAngle.setter
    def RollAngle(self, cmp):
        """The RollAngle (write)."""
        self._RollAngle = cmp

    @property
    def RollRate(self):
        """The RollRate (read-only)."""
        return self._RollRate

    @RollRate.setter
    def RollRate(self, cmp):
        """The RollRate (write)."""
        self._RollRate = cmp

    @property
    def Heading(self):
        """The Heading (read-only)."""
        return self._Heading

    @Heading.setter
    def Heading(self, cmp):
        """The Heading (write)."""
        self._Heading = cmp

    @property
    def x(self):
        """The x (read-only)."""
        return self._x

    @x.setter
    def x(self, cmp):
        """The x (write)."""
        self._x = cmp

    @property
    def y(self):
        """The y (read-only)."""
        return self._y

    @y.setter
    def y(self, cmp):
        """The y (write)."""
        self._y = cmp


class shipAction(object):
    def __init__(self):

        self.name= "shipAction"
        self._windDirection= 0.0
        self._windSpeed= 0.0


    @property
    def windDirection(self):
        """The windDirection (read-only)."""
        return self._windDirection

    @windDirection.setter
    def windDirection(self, cmp):
        """The windDirection (write)."""
        self._windDirection = cmp

    @property
    def windSpeed(self):
        """The windSpeed (read-only)."""
        return self._windSpeed

    @windSpeed.setter
    def windSpeed(self, cmp):
        """The windSpeed (write)."""
        self._windSpeed = cmp


class predictedPath(object):
    def __init__(self):

        self.name= "predictedPath"
        self._Confidence= 0.0
        self._Waypoints= 0.0


    @property
    def Confidence(self):
        """The Confidence (read-only)."""
        return self._Confidence

    @Confidence.setter
    def Confidence(self, cmp):
        """The Confidence (write)."""
        self._Confidence = cmp

    @property
    def Waypoints(self):
        """The Waypoints (read-only)."""
        return self._Waypoints

    @Waypoints.setter
    def Waypoints(self, cmp):
        """The Waypoints (write)."""
        self._Waypoints = cmp


class AnomalyMessage(object):
    def __init__(self):

        self.name= "AnomalyMessage"
        self._Anomaly= None


    @property
    def Anomaly(self):
        """The Anomaly (read-only)."""
        return self._Anomaly

    @Anomaly.setter
    def Anomaly(self, cmp):
        """The Anomaly (write)."""
        self._Anomaly = cmp


class legitimateMessage(object):
    def __init__(self):

        self.name= "legitimateMessage"
        self._legitimate= None


    @property
    def legitimate(self):
        """The legitimate (read-only)."""
        return self._legitimate

    @legitimate.setter
    def legitimate(self, cmp):
        """The legitimate (write)."""
        self._legitimate = cmp


