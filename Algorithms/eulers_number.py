def calc_next_digit_of_euler(current_sum, n):
    """
    Calculate the next digit of Euler's number (e) using its series expansion.
    
    :param current_sum: The current sum of the series.
    :param n: The current term index (starting from 0).
    :return: The next digit of e.
    """
    # Base case: if n is 0, return the first digit of e
    if n == 0:
        return 2  # e starts with 2.718...

    # Calculate the next term in the series
    next_term = 1 / factorial(n)  # n! (factorial) grows quickly, ensuring performance

    # Update the current sum
    current_sum += next_term

    # Return the next digit after the decimal point
    return int(next_term)  # Get the next digit after the decimal point

def factorial(n):
    """Compute factorial of n using an iterative approach for better performance."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
