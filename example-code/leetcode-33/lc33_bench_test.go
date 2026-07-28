package lc33bench

import (
	"fmt"
	"math/rand/v2"
	"slices"
	"testing"
)

// --- Solution 1: Linear Scan ---

func searchLinear(nums []int, target int) int {
	return slices.Index(nums, target)
}

// --- Solution 2: Modified Binary Search ---

func searchBinary(nums []int, target int) int {
	left, right := 0, len(nums)-1

	for left <= right {
		mid := left + (right-left)/2

		if nums[mid] == target {
			return mid
		}

		if nums[left] <= nums[mid] {
			if nums[left] <= target && target < nums[mid] {
				right = mid - 1
			} else {
				left = mid + 1
			}
		} else {
			if nums[mid] < target && target <= nums[right] {
				left = mid + 1
			} else {
				right = mid - 1
			}
		}
	}

	return -1
}

// --- Helpers ---

// buildInput returns the values 0..n-1 sorted and then rotated left by a
// seeded random amount, matching the problem's input format.
func buildInput(n int) []int {
	rng := rand.New(rand.NewPCG(42, uint64(n)))

	sorted := make([]int, n)
	for i := range sorted {
		sorted[i] = i
	}

	shift := rng.IntN(n)
	rotated := make([]int, 0, n)
	rotated = append(rotated, sorted[shift:]...)
	rotated = append(rotated, sorted[:shift]...)

	return rotated
}

// presentTarget is the value sitting at the middle of the rotated slice, so a
// linear scan always does exactly n/2 comparisons. That is the average case,
// and it is deterministic across runs.
func presentTarget(nums []int) int {
	return nums[len(nums)/2]
}

// missingTarget is never in the slice, so a linear scan always does n
// comparisons. That is the worst case.
const missingTarget = -1

// --- Unit Tests ---

func TestSolutions(t *testing.T) {
	for n := 100; n <= 1000; n += 100 {
		nums := buildInput(n)

		for _, target := range []int{presentTarget(nums), missingTarget} {
			got1 := searchLinear(nums, target)
			got2 := searchBinary(nums, target)
			if got1 != got2 {
				t.Errorf("n=%d target=%d: Linear=%d Binary=%d", n, target, got1, got2)
			}
		}
	}
}

// --- Benchmarks ---

var sink int

func benchmarkSolution(b *testing.B, fn func([]int, int) int, present bool) {
	for _, n := range []int{100, 200, 300, 400, 500, 600, 700, 800, 900, 1000} {
		nums := buildInput(n)

		target := missingTarget
		if present {
			target = presentTarget(nums)
		}

		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for b.Loop() {
				sink = fn(nums, target)
			}
		})
	}
}

func BenchmarkLinearPresent(b *testing.B) { benchmarkSolution(b, searchLinear, true) }
func BenchmarkBinaryPresent(b *testing.B) { benchmarkSolution(b, searchBinary, true) }
func BenchmarkLinearMissing(b *testing.B) { benchmarkSolution(b, searchLinear, false) }
func BenchmarkBinaryMissing(b *testing.B) { benchmarkSolution(b, searchBinary, false) }
