class Decision():
    def __init__(self,clip_name='None',a_type='None',d_type='None',a_parameter=-1,fps =24.0, bitrate = 1000.0, others=[0,0,0]):
        self.clip_name = clip_name
        self.a_type = a_type
        self.d_type = d_type
        self.a_param = a_parameter
        self.fps = fps
        self.bitrate = bitrate
        ## Here we use others to pass [a_param_0, a_param_1, raw_size]
        self.others = others
    


        