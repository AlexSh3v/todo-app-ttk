import time
from dataclasses import dataclass, field
import json
import pathlib
import pprint
import random
import textwrap


def load_tasks(p: pathlib.Path):

    if not p.exists():
        return []

    with p.open() as json_file:
        data = json.load(json_file)

    if isinstance(data, dict):
        return [{'id': k, **v} for k, v in data.items()]

    return data


def save_tasks(p: pathlib.Path, data: list):
    with p.open('w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


@dataclass
class TaskManager:
    tasks: list[dict] = field(default_factory=list)
    savefile: pathlib.Path = pathlib.Path(__file__).parent / 'tasks.json'

    def __post_init__(self):
        self.tasks = load_tasks(self.savefile)

    def save(self):
        save_tasks(self.savefile, self.tasks)

    def __get_ids(self) -> set:
        return {it['id'] for it in self.tasks}

    def generate_unique_id(self):
        number = random.randint(100, 999)
        ids = self.__get_ids()
        while number in self.tasks:
            number = random.randint(100, 999)
        return str(number)

    def print(self, show_position=False):
        s = '{} {}   {}'
        if len(self.tasks) == 0:
            print('~~ No tasks.')
            return
        for i, task in enumerate(self.tasks):
            id_ = task['id']
            text = textwrap.wrap(task['name'], width=30, break_long_words=True)
            check = '✓' if task['is_completed'] else ' '
            if show_position:
                check = i+1
            print(s.format(check, id_, text[0]))
            for t in text[1:]:
                print(s.format(' ', '   ', t))

    def add_task(self, task_name: str, is_completed: bool):
        id_ = self.generate_unique_id()
        self.tasks.append({
            'id': id_,
            'name': task_name,
            'is_completed': is_completed,
        })
    
    def delete_task(self, task_id: str) -> bool:

        task_to_delete = None
        for task in self.tasks:
            if task['id'] == task_id:
                task_to_delete = task
                break

        if task_to_delete is None:
            return False

        self.tasks.remove(task_to_delete)
        return True

    def mark_task(self, task_id: str) -> bool:
        task = self.search_by_id(task_id)

        if task is None:
            return False

        flag = task['is_completed']
        task['is_completed'] = not flag
        return True

    def search_by_id(self, task_id: str) -> dict | None:
        for task in self.tasks:
            if task['id'].startswith(task_id):
                return task
        return None

    def move(self, task_id, new_index) -> bool:
        task = self.search_by_id(task_id)
        if task is None:
            return False
        if not (0 <= new_index < len(self.tasks)):
            return False
        self.tasks.remove(task)
        self.tasks.insert(new_index, task)
        return True


if __name__ == '__main__':
    task_manager = TaskManager()
    while 1:
        task_manager.print()
        q = input('(A)dd, (E)dit, (D)elete, (q)Mark, (M)ove, (z)Quit\n'
                  '> ').lower()
        if q == 'a':
            name = input('Task Name> ')
            task_manager.add_task(name, False)
            task_manager.save()
        elif q == 'e':
            pass
        elif q == 'd':
            q_id = input('id> ')
            r = task_manager.delete_task(q_id)
            if r:
                print('[i] Delete success.')
                task_manager.save()
            else:
                print('[!] Not found task id.')
            time.sleep(1)
        elif q == 'q':
            q_id = input('id> ')
            if task_manager.mark_task(q_id):
                print('[i] Task marked!')
            else:
                print('[!] Not found task id!')
        elif q == 'm':
            task_manager.print(show_position=True)
            q_id = input('id> ')
            pos = int(input('pos> '))
            task_manager.move(q_id, pos-1)
            task_manager.save()
        elif q == 'z':
            print('[i] Bye.')
            quit()

