# Day 09 - Largest Rectangle from Red Tiles

def main():
    # Update the path to your actual Advent of Code input file
    INPUT_PATH = "E:\Advent of Code\AOC 25\Day-09\input.txt"

    points = []

    # Read all points from the file
    with open(INPUT_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Expect lines like: x,y
            x_str, y_str = line.split(",")
            x = int(x_str)
            y = int(y_str)
            points.append((x, y))

    n = len(points)
    if n < 2:
        # Not enough points to form a rectangle
        print(0)
        return

    max_area = 0

    # Check every pair of points as opposite corners of an axis-aligned rectangle
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # Width and height are inclusive of both corners
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height

            if area > max_area:
                max_area = area

    print(max_area)


if __name__ == "__main__":
    main()