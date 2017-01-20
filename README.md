# MCM2017_TSASecurity
TSA Queue simulation for the Mathematical Contest in Modeling (MCM) 2017

To get started (Using Linux):
Assuming you have already cloned the repo to where you want it 
and have additionally naviagated to it. Run the following commands.

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python test.py

If the first command failed -- download python3
If the second command failed -- google it.
If the third command failed: 
   And no graph was output, you need to reconfigure matplotlib.
   Run the command:

   python -c 'print(); import matplotlib; import matplotlib.pyplot; print(matplotlib.backends.backend + "\n"); matplotlib.matplotlib_fname()'

   The first line should read agg. 
   The second line should be the location of the matplotlibrc file. 
   Open that file and change your backend from agg to TkAgg. 
   Retry the test script.


   