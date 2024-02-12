from io import StringIO
import pytest

def real_file_operation():
    with open('new_file.txt', 'w') as f:
        f.write("Hello, world!")
        # f.close is not actually necessary in this case, because the context manager will handle it
        # f.close()


def simulated_file_like_object_operation():
    # We can do all the same operations (use the same APIs)
    # but in memory, without a real file being created or modified
    # (this is faster, and less complicated, less likely to have problems)
    with StringIO() as fake_file:

        fake_file.write("Hello, world!")
        fake_file.flush()

        fake_file.seek(0)
        print(fake_file.read())

        fake_file.close()

if __name__ == '__main__':

    simulated_file_like_object_operation()

def hello():
    print("Hello!")
