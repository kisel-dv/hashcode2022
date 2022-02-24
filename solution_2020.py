import time
import random

books_score = {}
libraries = {}
books_cnt = 0
libraries_cnt = 0
duration = 0

class CustomWriter():
    def __init__(self, file):
        self.file = file

    def writeline(self, line):
        self.file.write(f'{line}\n')


class Library():
    def __init__(self, books_cnt, signup, books_per_day):
        self.books_cnt = books_cnt
        self.signup = signup
        self.books_per_day = books_per_day
        self.books = []

    def get_books(self, n):
        return self.books[:n]

    def get_new_books(self, n, processed_books):
        books = []
        for b in self.books:
            if len(books) >= n:
                break
            if b in processed_books:
                continue
            books.append(b)
        return books


def read(filepath):
    global books_cnt, libraries_cnt, duration
    with open(filepath, 'r') as f:
        books_cnt, libraries_cnt, duration = map(int, f.readline().strip('\n').split(' '))
        books_scores_arr = f.readline().strip('\n').split(' ')
        for i in range(books_cnt):
            books_score[i] = int(books_scores_arr[i])

        for i in range(libraries_cnt):
            books_cnt, signup, books_per_day = map(int, f.readline().strip('\n').split(' '))
            library = Library(books_cnt, signup, books_per_day)
            books = list(map(int, f.readline().strip('\n').split(' ')))
            library.books = sorted(books, key=books_score.get, reverse=True)
            libraries[i] = library
    return


def simulation(libraries_order):
    processed_books = set()
    available_time = [-1 for _ in libraries]
    # available_time = [[] for _ in libraries]
    ready_libs = set()

    score = 0
    signup_end_time = -1
    for s in range(duration):
        for lib in libraries_order:
            if s < available_time[lib]:
                continue

            if lib not in ready_libs:
                if s < signup_end_time:
                    continue
                signup_end_time = libraries[lib].signup + s
                available_time[lib] = libraries[lib].signup + s
                ready_libs.add(lib)
                continue

            new_books = libraries[lib].get_new_books(libraries[lib].books_per_day, processed_books)
            for book in new_books:
                if book not in processed_books:     # возможно не нужно - там вроде только книжки, которых не было
                    score += books_score[book]
            processed_books.update(new_books)
        # print(f'time: {s}, score: {score}')
        # print(ready_libs)
        # print(processed_books)
    # print(f'time: {s}, score: {score}')
    return score, len(ready_libs)


def get_submission(libraries_order):
    global duration
    with open('submission.txt', 'w') as f:
        writer = CustomWriter(f)
        writer.writeline(f'{len(libraries_order)}')
        scanning_time = 0
        for lib in libraries_order:
            scanning_time += libraries[lib].signup
            if scanning_time > duration:
                break
            signed_books_cnt = min(libraries[lib].books_cnt, (duration - scanning_time) * libraries[lib].books_per_day)
            writer.writeline(f'{lib}, {signed_books_cnt}')
            lib_books = libraries[lib].get_books(signed_books_cnt)
            # print(" ".join([str(b) for b in lib_books]))
            writer.writeline(f'{" ".join([str(b) for b in lib_books])}')


DATA_DIR = './data'
DATA_FILES = [f'{DATA_DIR}/{x}.in' for x in 'abcdef']


def main():
    score = 4109300
    for file in DATA_FILES:
        if file == './data/d.in':
            continue
        read(file)


        default_order = list(libraries.keys())
        curr_score, curr_libs = simulation(default_order)
        best_curr_score = curr_score
        print(f'{file}\t current score: {curr_score}, libs scanned : {curr_libs}/{len(libraries)}')

        ordered_by_signup = sorted(default_order, key=lambda x: libraries[x].signup)
        curr_score, curr_libs = simulation(ordered_by_signup)
        print(f'{file}\t current score: {curr_score}, libs scanned : {curr_libs}/{len(libraries)}')
        if curr_score > best_curr_score:
            best_curr_score = curr_score

        # print(f'default_score:{best_curr_score}')
        # if file == './data/c.in':
        #     score += best_curr_score
        #     continue
        # for _ in range(50):
        #     shuffled_order = default_order
        #     random.shuffle(shuffled_order)
        #     curr_score = simulation(shuffled_order)
        #     if curr_score > best_curr_score:
        #         print(f'boom +{curr_score - best_curr_score}')
        #         best_curr_score = curr_score


        score += best_curr_score
        # print(f'best score: {best_curr_score}, libs scanned : {curr_libs}/{len(libraries)}')
    print(f'total score: {score}')


if __name__ == '__main__':
    main()