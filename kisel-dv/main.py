# input

files = [f'../input_data/{x}.txt' for x in 'abcdef']


class Contributor:
    def __init__(self, skills):
        self.skills = skills


class Project:
    def __init__(self,  days, score, best_before_day, roles):
        self.days = days
        self.score = score
        self.best_before_day = best_before_day
        self.roles = roles


contributors = {}
projects = {}

# equal lvl for each skill
eq_skills_to_contribs = {}
# great or equal lvl for each skill
geq_skills_to_contribs = {}


def read_file(file_path):
    with open(file_path, 'r') as f:
        # c, p
        n_contributors, n_projects = map(int, f.readline().strip().split(' '))
        for i in range(n_contributors):
            name, n_skills = f.readline().strip().split(' ')
            n_skills = int(n_skills)
            curr_skills = {}
            for j in range(n_skills):
                skill_name, skill_level = f.readline().strip().split(' ')
                skill_level = int(skill_level)
                curr_skills[skill_name] = skill_level

            contributors[name] = Contributor(curr_skills)
        for i in range(n_projects):
            name, days, score, best_before_day, n_roles = f.readline().strip().split(' ')
            days, score, best_before_day, n_roles = int(days), int(score), int(best_before_day), int(n_roles)
            curr_roles = {}
            for j in range(n_roles):
                skill_name, skill_level = f.readline().strip().split(' ')
                skill_level = int(skill_level)
                curr_roles[skill_name] = skill_level
            projects[name] = Project(days, score, best_before_day, curr_roles)

    return contributors, projects


file_name = '../input_data/a.txt'
contributors, projects = read_file(file_name)


def print_res(output_file):
    pass