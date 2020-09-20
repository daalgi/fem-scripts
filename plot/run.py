import openseespy.postprocessing.Get_Rendering as opsplt   # Using updated OpenSeesPy
# import openseespyvis.Get_Rendering as opsplt      # Using openseespyvis package

opsplt.plot_model("node", Model="CantiBeam")
opsplt.plot_deformedshape(Model="CantiBeam",LoadCase="Push", overlap="no", tstep=2.0, scale=1.0)
opsplt.plot_deformedshape(Model="CantiBeam",LoadCase="Push", overlap="no", scale=1.0)
ani=opsplt.animate_deformedshape(Model="CantiBeam",LoadCase="Push",dt=0.01, scale=1, timeScale=10, 
                                                                              Movie = "CantiBeam")