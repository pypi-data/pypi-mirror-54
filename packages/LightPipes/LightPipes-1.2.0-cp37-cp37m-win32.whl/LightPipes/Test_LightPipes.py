#TEST_LightPipes
import _LightPipes
import matplotlib.pyplot as plt

m=1
mm=1e-3*m
um=1e-6*m
cm=1e-2*m
LP=_LightPipes.Init()
wavelength=20*um
size=30.0*mm
N=501

#LPhelp()
F=LP.Begin(size,wavelength,N)
F=LP.GaussBeam(size,wavelength,N,size/40,0.0,0)
#F1=LP.PointSource(size,wavelength,N,-0.6*mm,0)
#F2=LP.PointSource(size,wavelength,N, 0.6*mm,0)

F1=LP.CircAperture(0.15*mm, -0.6*mm,0, F)
F2=LP.CircAperture(0.15*mm, 0.6*mm,0, F)    
F=LP.BeamMix(F1,F2)
F=LP.Forvard(10*cm,F)
I=LP.Intensity(0,F)

#print("Execution time: --- %4.2f seconds ---" % (time.time() - start_time))   
plt.imshow(I,cmap='rainbow');plt.axis('off')
plt.show()
