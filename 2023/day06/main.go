package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Race struct {
	time int
	dist int
}

func readLines(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}

func calcHoldDist(hold, time int) int {
	if hold == 0 || hold >= time {
		return 0
	}

	return hold * (time - hold)
}

func run() error {
	lines, err := readLines(os.Args[1])
	if err != nil {
		return err
	}

	times := strings.Fields(lines[0])[1:]
	dists := strings.Fields(lines[1])[1:]

	var races []Race
	for i := 0; i < len(times); i++ {
		t, err := strconv.Atoi(times[i])
		if err != nil {
			return err
		}

		d, err := strconv.Atoi(dists[i])
		if err != nil {
			return err
		}

		race := Race{
			time: t,
			dist: d,
		}
		races = append(races, race)
	}

	// PART 1
	// total := 1
	// for _, race := range races {
	// 	wins := 0
	// 	for i := 0; i < race.time; i++ {
	// 		dist := calcHoldDist(i, race.time)
	// 		if dist > race.dist {
	// 			wins++
	// 		}
	// 	}
	// 	total *= wins
	// }

	// PART 2
	total := 0
	var bigtime, bigdist string
	for _, race := range races {
		bigtime += strconv.Itoa(race.time)
		bigdist += strconv.Itoa(race.dist)
	}

	time, err := strconv.Atoi(bigtime)
	if err != nil {
		return err
	}

	dist, err := strconv.Atoi(bigdist)
	if err != nil {
		return err
	}

	for i := 0; i < time; i++ {
		d := calcHoldDist(i, time)
		if d > dist {
			total++
		}
	}

	fmt.Println(total)
	return nil
}

func main() {
	code := 0

	err := run()
	if err != nil {
		fmt.Println(err)
		code = 1
	}

	os.Exit(code)
}
