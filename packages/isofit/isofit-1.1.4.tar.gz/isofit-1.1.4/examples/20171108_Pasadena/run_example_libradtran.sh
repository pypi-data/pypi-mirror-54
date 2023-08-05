# David R Thompson

# Create surface model
python3 ../../utils/surfmodel.py configs/ang20171108t184227_surface.json

# Run experiment
python3 ../../isofit/isofit.py --level DEBUG configs/ang20171108t184227_beckmanlawn-libradtran.json 

