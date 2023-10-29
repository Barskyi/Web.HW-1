from Bot import Bot
from abc import ABC

class AbstractPrint(ABC):
    def run(self):
        pass

class ContactAssistant(AbstractPrint):
    def __init__(self):
        self.bot = Bot()

    def run(self):
        print('Hello. I am your contact-assistant. What should I do with your contacts?')
        self.bot.book.load("auto_save")
        commands = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Congratulate', 'View', 'Exit']
        while True:
            action = input('Type help for list of commands or enter your command\n').strip().lower()
            if action == 'help':
                format_str = str('{:%s%d}' % ('^', 20))
                for command in commands:
                    print(format_str.format(command))
                action = input().strip().lower()
                self.bot.handle(action)
                if action in ['add', 'remove', 'edit']:
                    self.bot.book.save("auto_save")
            else:
                self.bot.handle(action)
                if action in ['add', 'remove', 'edit']:
                    self.bot.book.save("auto_save")
            if action == 'exit':
                break

if __name__ == "__main__":
    assistant = ContactAssistant()
    assistant.run()
