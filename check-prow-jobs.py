#!/usr/bin/python

import glob
import os
import re

class PeriodicJob():
    def __init__(self, auto_repo='openshift/openshift-tests-private', repo_root='/home/lxia/codes/github.com/release'):
        self.auto_repo = auto_repo
        self.repo_root = repo_root
        self.job_path = os.path.join(repo_root, 'ci-operator/jobs', auto_repo)
        self.jobs = []

    def get_jobs(self, pattern='periodic-ci-', force=False):
        if force:
            regex = re.compile(pattern)
            self.jobs.clear()
            for f in glob.glob(self.job_path + "/*-periodics.yaml", recursive=False):
                with open(f) as _fobj:
                    for line in _fobj.readlines():
                        if regex.search(line):
                            self.jobs.append(line.split(':')[1].strip())
            self.jobs.sort(reverse=True)
        elif len(self.jobs) == 0:
            self.get_jobs(pattern, force=True)

    def count_jobs(self, patterns):
        self.get_jobs()
        statements = []
        statements.append(f'Data for repo {self.auto_repo}\n')
        fqs = ('f360', 'f30', 'f28', 'f14', 'f7', 'f4', 'f3', 'f2', 'f1')
        for pattern in patterns:
            count = sum([pattern in job for job in self.jobs])
            if count != 0:
                statements.append(f'\tTotal jobs for {pattern}: {count}\n')
            for fq in fqs:
                fq_count = sum([pattern in j and bool(re.search(fq+'\\b', j)) for j in self.jobs])
                if fq_count != 0:
                    statements.append(f"\t\t{fq+':':<4}{str(fq_count):>4}\n")
        statements.append(f'Total jobs for all version: {len(self.jobs)}\n')
        print(*statements)

versions = list(range(16, 10, -1))
patterns = ['release-4.' + str(s) for s in versions]
patterns.append('master')
cix = PeriodicJob()
cix.count_jobs(patterns)
ciy = PeriodicJob(auto_repo='openshift/verification-tests')
ciy.count_jobs(patterns)
