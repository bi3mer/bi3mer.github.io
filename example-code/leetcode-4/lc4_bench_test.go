package lc4bench

import (
	"fmt"
	"math"
	"math/rand/v2"
	"slices"
	"testing"
)

func makeSortedArray(rng *rand.Rand, n int) []int {
	s := make([]int, n)
	for i := range s {
		s[i] = rng.Int()
	}
	slices.Sort(s)
	return s
}

// --- solutions ---

func medianOf(nums []int) float64 {
	mid := len(nums) / 2
	if len(nums)%2 == 0 {
		return float64(nums[mid-1]+nums[mid]) / 2.0
	}
	return float64(nums[mid])
}

func dumbSolution(nums1, nums2 []int) float64 {
	combined := append(nums1, nums2...)
	slices.Sort(combined)
	return medianOf(combined)
}

func twoPointers(nums1, nums2 []int) float64 {
	size := len(nums1) + len(nums2)
	half := size / 2
	i1, i2 := 0, 0
	prev, cur := 0, 0

	for range half + 1 {
		prev = cur
		if i1 < len(nums1) {
			if i2 < len(nums2) {
				if nums1[i1] <= nums2[i2] {
					cur = nums1[i1]
					i1++
				} else {
					cur = nums2[i2]
					i2++
				}
			} else {
				cur = nums1[i1]
				i1++
			}
		} else {
			cur = nums2[i2]
			i2++
		}
	}

	if size%2 == 0 {
		return float64(prev+cur) / 2.0
	}
	return float64(cur)
}

func binarySearch(nums1, nums2 []int) float64 {
	a, b := nums1, nums2
	if len(nums1) > len(nums2) {
		a, b = nums2, nums1
	}

	aLeft, aRight := math.MinInt, math.MaxInt
	bLeft, bRight := math.MinInt, math.MaxInt
	size := len(a) + len(b)
	half := size / 2
	lo, hi := 0, len(a)

	for lo <= hi {
		i1 := (hi + lo) / 2
		i2 := half - i1

		aLeft, aRight = math.MinInt, math.MaxInt
		bLeft, bRight = math.MinInt, math.MaxInt

		if i1 > 0 {
			aLeft = a[i1-1]
		}
		if i1 < len(a) {
			aRight = a[i1]
		}
		if i2 > 0 {
			bLeft = b[i2-1]
		}
		if i2 < len(b) {
			bRight = b[i2]
		}

		if aLeft > bRight {
			hi = i1 - 1
		} else if aRight < bLeft {
			lo = i1 + 1
		} else {
			break
		}
	}

	if size%2 == 0 {
		left := max(aLeft, bLeft)
		right := min(aRight, bRight)
		return float64(left+right) / 2.0
	}
	return float64(min(aRight, bRight))
}

// --- tests ---

func TestSolutions(t *testing.T) {
	for _, n := range []int{1000, 10000, 100000} {
		rng := rand.New(rand.NewPCG(42, uint64(n)))
		a := makeSortedArray(rng, n)
		bb := makeSortedArray(rng, n)

		want := dumbSolution(a, bb)
		got1 := twoPointers(a, bb)
		got2 := binarySearch(a, bb)

		if got1 != want {
			t.Errorf("n=%d twoPointers: got %v want %v", n, got1, want)
		}
		if got2 != want {
			t.Errorf("n=%d binarySearch: got %v want %v", n, got2, want)
		}
	}
}

var sink float64

const numInputPairs = 64

type inputPair struct{ a, b []int }

func benchmarkMedian(b *testing.B, fn func([]int, []int) float64) {
	for _, n := range []int{1000, 10000, 100000} {
		rng := rand.New(rand.NewPCG(42, uint64(n)))
		pairs := make([]inputPair, numInputPairs)
		for i := range pairs {
			pairs[i] = inputPair{makeSortedArray(rng, n), makeSortedArray(rng, n)}
		}
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			idx := 0
			for b.Loop() {
				sink = fn(pairs[idx].a, pairs[idx].b)
				idx = (idx + 1) % numInputPairs
			}
		})
	}
}

func BenchmarkDumb(b *testing.B)         { benchmarkMedian(b, dumbSolution) }
func BenchmarkTwoPointers(b *testing.B)  { benchmarkMedian(b, twoPointers) }
func BenchmarkBinarySearch(b *testing.B) { benchmarkMedian(b, binarySearch) }
