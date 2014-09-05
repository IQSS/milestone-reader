from __future__ import print_function

from datetime import datetime, date
from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from milestone_reader.utils.msg_util import *

from apps.repositories.models import Repository
from apps.milestones.models import Milestone

class RepoMilestoneMonthsOrganizer:
    """Repo milestones for a given month"""

    NO_DUE_DATE = 'NO_DUE_DATE'
    def __init__(self, repo):
        self.repo = repo
        self.month_milestones = {} #  { month : [milestone, milestone, milestone }

    def show(self):
        for mm, mm_list in self.month_milestones.items():
            msg('%s' % mm)
            msg(mm_list)

    def get_milestones_for_month(self, month_obj):
        if month_obj is None:
            return None
        return self.month_milestones.get(month_obj, None)


    @staticmethod
    def get_milestone_month(ms):
        if not type(ms) is Milestone:
            raise TypeError('Not a milestone')

        if not ms.due_on:
            return RepoMilestoneMonthsOrganizer.NO_DUE_DATE

        return date(ms.due_on.year, ms.due_on.month, 1)

    def add_milestone(self, ms):
        if not type(ms) is Milestone:
            raise TypeError('Not a milestone')

        ms_month_key = RepoMilestoneMonthsOrganizer.get_milestone_month(ms)
        month_list = self.month_milestones.get(ms_month_key, [])
        month_list.append(ms)
        self.month_milestones[ms_month_key] = month_list
        #if not ms_month:
        #    self.month_milestones.setdefault(self.NO_DUE_DATE, []).append(ms)
        #else:
        #    self.month_milestones.setdefault(ms_month, []).append(ms)

class MonthMilestones:
    """Used for template display"""

    def __init__(self, month, milestones):
        self.month = month
        self.milestones = milestones

class MilestoneMonthOrganizer:
    """Organize milestones by month and repository"""

    def __init__(self, milestones):
        self.current_date = datetime.now()
        self.repo_lookups = {}      # { repository : RepoMilestoneMonthsOrganizer }
        self.month_list = []

        #self.sorted_repos = []
        self.organize_milestones(milestones)

    def show(self):
        for repo, organizer in self.repo_lookups.items():
            msgt(repo)
            organizer.show()

    def get_sorted_repos(self):
        repos  = self.repo_lookups.keys()
        repos.sort(key=lambda x: x.display_order)
        return repos


    def get_organized_months(self, descending_order=False):
        msgt('get_organized_months')
        """
        Display
            month 1 [ repo 1 MonthMilestones  ]  [ repo 2 MonthMilestones  ]  [  repo 3 MonthMilestones ]
            month 2 [ repo 1 MonthMilestones  ]  [ repo 2 MonthMilestones  ]  [  repo 3 MonthMilestones ]
            month 3 [ repo 1 MonthMilestones  ]  [ repo 2 MonthMilestones  ]  [  repo 3 MonthMilestones ]
        """

        month_milestone_list = []

        #[ [MonthMilestones, MonthMilestones, MonthMilestones]
        #  [MonthMilestones, MonthMilestones, MonthMilestones]
        # ]
        repos  = self.get_sorted_repos()
        for month_obj in self.month_list:
            #msg('Month: %s' % month_obj )
            single_month_list = []  #  [ repo 1 MonthMilestones  ]  [ repo 2 MonthMilestones  ]  [  repo 3 MonthMilestones ] ...
            # create single row for the current month
            for repo in repos:
                #msg('-- repo: %s' % repo)

                repo_milestone_months_organizer = self.repo_lookups.get(repo, None)
                if repo_milestone_months_organizer is None:
                    #msg('   no organizer for this repo (wrong!)')
                    single_month_list.append(MonthMilestones(month_obj, None))   # No milestones for this repo/month
                else:
                    #msg('   should be milestones')
                    repo_milestones = repo_milestone_months_organizer.get_milestones_for_month(month_obj)
                    if repo_milestones is None:
                        #msg('   no milestones found')
                        single_month_list.append(MonthMilestones(month_obj, None))
                    else:
                        msg('   milestones found: %s' % repo_milestones)
                        single_month_list.append(MonthMilestones(month_obj, repo_milestones))   # No milestones for this repo/month
            month_milestone_list.append(single_month_list)

        dashes()
        if descending_order:
            month_milestone_list.reverse()
        return month_milestone_list

    def organize_milestones(self, milestones):
        if milestones is None:
            raise TypeError('milestones is None')

        cnt = 0
        last_ms = None
        for ms in milestones:
            if not type(ms) is Milestone:
                raise TypeError('ms is not a Milestone')
            cnt += 1

            if ms.due_on:
                ms.days_remaining = ms.due_on.replace(tzinfo=None) - self.current_date#.date()

            if ms.repository.parent_repository:
                main_ms_repo = ms.repository.parent_repository
            else:
                main_ms_repo = ms.repository

            repo_milestone_organizer = self.repo_lookups.get(main_ms_repo, None)
            if repo_milestone_organizer is None:
                repo_milestone_organizer = RepoMilestoneMonthsOrganizer(main_ms_repo)
            repo_milestone_organizer.add_milestone(ms)
            self.repo_lookups[main_ms_repo] = repo_milestone_organizer

            fmt_month = RepoMilestoneMonthsOrganizer.get_milestone_month(ms)
            if not fmt_month in self.month_list:
                self.month_list.append(fmt_month)


