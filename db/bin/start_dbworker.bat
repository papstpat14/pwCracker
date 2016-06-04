cd ..
for /L %%N IN (1, 1, %1) DO start cmd /k python ./worker.py %2