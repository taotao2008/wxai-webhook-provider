import concurrent.futures

def test_threading():
    arg1 = "1"
    result = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_result = executor.submit(task, arg1)
        result = future_result.result()
        print(result)

def task(arg1):
    # Do some work
    return "hello1"
if __name__ == '__main__':
    test_threading()