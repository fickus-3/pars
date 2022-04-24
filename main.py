from hh import get_jobs as hh_get_jobs
from save import save_to_csv

hh_jobs = hh_get_jobs()

save_to_csv((hh_jobs))



