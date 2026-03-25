#!/bin/bash
# Lab 03 - Shell Scripting Examples

# Example 1: Hello World
echo "=== Example 1: Hello World ==="
echo "HELLO"

# Example 2: Loop - print odd numbers 1-99
echo ""
echo "=== Example 2: Odd numbers 1-99 ==="
for ((i=1; i<=99; i=i+2)); do
    echo -n "$i "
done
echo ""

# Example 3: Read name and greet
echo ""
echo "=== Example 3: Greeting ==="
echo -n "Enter your name: "
read NAME
echo "Welcome $NAME"

# Example 4: Arithmetic operations
echo ""
echo "=== Example 4: Arithmetic ==="
echo -n "Enter NUM1: "
read NUM1
echo -n "Enter NUM2: "
read NUM2
echo "Addition:       $(expr $NUM1 + $NUM2)"
echo "Subtraction:    $(expr $NUM1 - $NUM2)"
echo "Multiplication: $(expr $NUM1 \* $NUM2)"
echo "Division:       $(expr $NUM1 / $NUM2)"

# Example 5: Comparison
echo ""
echo "=== Example 5: Comparison ==="
echo -n "Enter X: "
read X
echo -n "Enter Y: "
read Y
if (( X > Y )); then
    echo "X is greater than Y"
elif (( X == Y )); then
    echo "X is equal to Y"
else
    echo "X is less than Y"
fi

# Example 6: Yes/No input
echo ""
echo "=== Example 6: Yes/No ==="
echo -n "Enter y or n: "
read word
if [[ ($word == 'y') || ($word == 'Y') ]]; then
    echo "YES"
elif [[ ($word == 'n') || ($word == 'N') ]]; then
    echo "NO"
else
    echo "Invalid input"
fi

# Example 7: Floating point
echo ""
echo "=== Example 7: Float input ==="
echo -n "Enter a decimal number: "
read x
printf "Formatted: %.3f\n" $(echo "$x" | bc -l)

# Example 8: Average of N numbers
echo ""
echo "=== Example 8: Average ==="
echo -n "How many numbers? "
read num
ctr=$num
sum=0
while [ $ctr -gt 0 ]; do
    echo -n "Enter number: "
    read x
    sum=$((sum + x))
    ctr=$((ctr - 1))
done
printf "Average: %.3f\n" $(echo "$sum/$num" | bc -l)
