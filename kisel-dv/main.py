# input


class Contributor:
    def __init__(self, skills):
        self.skills = skills


class Project:
    def __init__(self,  days, score, best_before_day, roles):
        self.days = days
        self.score = score
        self.best_before_day = best_before_day
        self.roles = roles


# contributors = {}
# projects = {}
#
# # equal lvl for each skill
# eq_skills_to_contribs = {}
# # great or equal lvl for each skill
# geq_skills_to_contribs = {}


def read_file(file_path):
    contributors = {}
    projects = {}
    eq_skills_to_contribs = {}
    geq_skills_to_contribs = {}
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

                if skill_name not in eq_skills_to_contribs:
                    eq_skills_to_contribs[skill_name] = [[] for _ in range(101)]
                eq_skills_to_contribs[skill_name][skill_level].append(name)

                if skill_name not in geq_skills_to_contribs:
                    geq_skills_to_contribs[skill_name] = [[] for _ in range(101)]
                for lvl in range(0, skill_level + 1):
                    geq_skills_to_contribs[skill_name][lvl].append(name)


            contributors[name] = Contributor(curr_skills)
        for i in range(n_projects):
            name, days, score, best_before_day, n_roles = f.readline().strip().split(' ')
            days, score, best_before_day, n_roles = int(days), int(score), int(best_before_day), int(n_roles)
            curr_roles = []
            for j in range(n_roles):
                skill_name, skill_level = f.readline().strip().split(' ')
                skill_level = int(skill_level)
                curr_roles.append((skill_name, skill_level))
            projects[name] = Project(days, score, best_before_day, curr_roles)

    return contributors, projects, eq_skills_to_contribs, geq_skills_to_contribs


# TODO: add time_check
def get_score(projects, print=False):
    score = 0
    for proj in projects:
        if projects[proj].contributors:  # equal that the project is done
            score += projects[proj].score
    return score


def print_res(file_name, projects_done):
    with open(file_name, 'w') as f:
        f.write(f'{len(projects_done)}\n')
        for proj in projects_done:
            f.write(f'{list(proj.keys())[0]}\n')
            f.write(f'{" ".join(list(proj.values())[0])}\n')


def simulation(projects):
    # curr_time = 0
    # available = {}
    # while True:
    #     for proj in projects:
    #         for role in proj.roles:
    #
    #     curr_time += 1

    available = {}
    projects_done = []
    score = 0

    for contrib_name in contributors:
        available[contrib_name] = 0

    project_order = sorted(list(projects.keys()), key=lambda x: projects[x].best_before_day)

    curr_time = 0
    projects_done_set = set()
    while curr_time < 50:
        project_order = [x for x in project_order if x not in projects_done_set]
        for proj in project_order:
            curr_contributors = []
            potential_upgrade = {}
            failed = False
            # roles_order = sorted(projects[proj].roles, key=lambda x: x[1], reverse=True)

            # langs with decreased demands because of high skill conributors in proj
            top_level_by_skill = {}
            for role in projects[proj].roles:
                role_name = role[0]
                lvl = role[1]
                if role_name in top_level_by_skill:
                    if top_level_by_skill[role_name] >= lvl:
                        lvl -= 1
                found = False
                # contrib_name = min([x for x in eq_skills_to_contribs[role_name][lvl] if x not in curr_contributors],
                #                    key=lambda x: available[x], default=None)
                # if contrib_name is None:
                contrib_name = min([x for x in geq_skills_to_contribs[role_name][lvl] if x not in curr_contributors], key=lambda x: available[x], default=None)
                if contrib_name is not None:
                    curr_contributors.append(contrib_name)
                    if lvl == contributors[contrib_name].skills[role_name]:
                        potential_upgrade[contrib_name] = role_name
                    # available[contrib_name] += projects[proj].days
                    found = True

                    for sk in contributors[contrib_name].skills:
                        if sk not in top_level_by_skill:
                            top_level_by_skill[sk] = contributors[contrib_name].skills[sk]
                        elif contributors[contrib_name].skills[sk] >= top_level_by_skill[sk]:
                            top_level_by_skill[sk] = contributors[contrib_name].skills[sk]
                # for contrib_name in geq_skills_to_contribs[role_name][lvl]:
                    # if available[contrib_name]:
                    #     # projects[proj].contributors.append(contrib_name)
                    #     curr_contributors.append(contrib_name)
                    #     available[contrib_name] += projects[proj].days
                    #     found = True
                    #     break
                if not found:
                    failed = True
                    break
            if not failed:
                # for contrib_name in curr_contributors:
                #     available[contrib_name] -= projects[proj].days
            # else:
                # TODO: add time_check
                start_day = max([available[contrib_name] for contrib_name in curr_contributors])
                if start_day + projects[proj].days > projects[proj].score + projects[proj].best_before_day:
                    continue
                for contrib_name in curr_contributors:
                    available[contrib_name] = start_day + projects[proj].days
                for contrib_name in potential_upgrade:
                    upgraded_skill = potential_upgrade[contrib_name]
                    contributors[contrib_name].skills[upgraded_skill] += 1
                    new_level = contributors[contrib_name].skills[potential_upgrade[contrib_name]]
                    geq_skills_to_contribs[upgraded_skill][new_level].append(contrib_name)
                    eq_skills_to_contribs[upgraded_skill][new_level].append(contrib_name)
                    eq_skills_to_contribs[upgraded_skill][new_level-1].remove(contrib_name)

                    # TODO: не делаю пока в eq_skills_to_contribs
                score += max(min(projects[proj].score + projects[proj].best_before_day - (start_day + projects[proj].days), projects[proj].score), 0)
                projects_done.append({proj: curr_contributors})
                projects_done_set.add(proj)
        curr_time += 1

    return projects_done, score


total_score = 0
for file in 'abcdef':
    input_file = f'../input_data/{file}.txt'
    contributors, projects, eq_skills_to_contribs, geq_skills_to_contribs = read_file(input_file)

    curr_score = 0
    curr_projects_done = None
    for i, project_order in enumerate([sorted(list(projects.keys()), key=lambda x: projects[x].best_before_day),
                          sorted(list(projects.keys()), key=lambda x: projects[x].days),
                          sorted(list(projects.keys()), key=lambda x: projects[x].best_before_day - projects[x].days, reverse=True),
                        sorted(list(projects.keys()),
                                              key=lambda x: len(projects[x].roles)),
                        [x for x in projects if len(projects[x].roles) < 4],
                                       sorted([x for x in projects if projects[x].days < 1000]),
                          projects]):
        projects_done, score = simulation(projects)
        print(f'{file}, {i}, {score}')
        if score > curr_score:
            curr_score = score
            curr_projects_done = projects_done
            print('score_updated')
    total_score += score
    print(f'{file}: {score}')

    output_file = f'../output_data/{file}.txt'
    print_res(output_file, curr_projects_done)

print(total_score)
