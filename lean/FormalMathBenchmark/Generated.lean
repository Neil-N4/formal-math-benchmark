import Mathlib.Data.Int.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.NormNum
import FormalMathBenchmark.Examples

namespace FormalMathBenchmark.Generated

/- Problem: algebra_linear_system
   Topic: algebra
   Prompt: If x + y = 10 and xy = 21, find x^2 + y^2.
-/

/- Claim c1: Use the identity x^2 + y^2 = (x + y)^2 - 2xy. -/
theorem algebra_linear_system_sum_sq_identity (x y : Int) : x^2 + y^2 = (x + y)^2 - 2 * x * y := by
  simpa [mul_comm, mul_left_comm, mul_assoc] using FormalMathBenchmark.sum_sq_identity x y

/- Claim c2: Compute (x + y)^2 = 100. -/
theorem algebra_linear_system_sum_sq_substitution (x y : Int) (h : x + y = 10) : (x + y)^2 = 100 := by
  calc
    (x + y)^2 = (10 : Int)^2 := by simpa [h]
    _ = 100 := by norm_num

/- Claim c3: Compute x^2 + y^2 = 100 - 42 = 58. -/
theorem algebra_linear_system_algebra_linear_system_final (x y : Int) (hs : x + y = 10) (hxy : x * y = 21) : x^2 + y^2 = 58 := by
  calc
    x^2 + y^2 = (x + y)^2 - 2 * x * y := by
      simpa [mul_comm, mul_left_comm, mul_assoc] using FormalMathBenchmark.sum_sq_identity x y
    _ = (10 : Int)^2 - 2 * (x * y) := by
      rw [hs]
      ring
    _ = (10 : Int)^2 - 2 * 21 := by rw [hxy]
    _ = 58 := by norm_num


/- Problem: number_theory_divisibility
   Topic: number theory
   Prompt: Find the remainder when 6^4 + 6^3 + 6^2 + 6 + 1 is divided by 5.
-/

/- Claim c1: Reduce 6 modulo 5 to get 1. -/
theorem number_theory_divisibility_mod_reduce_six : 6 % 5 = 1 := by
  norm_num

/- Claim c2: Rewrite the expression modulo 5 as 1^4 + 1^3 + 1^2 + 1 + 1. -/
theorem number_theory_divisibility_mod_expression_rewrite : (6^4 + 6^3 + 6^2 + 6 + 1) % 5 = (1^4 + 1^3 + 1^2 + 1 + 1 : Nat) % 5 := by
  norm_num

/- Claim c3: Compute 1 + 1 + 1 + 1 + 1 = 5, and 5 mod 5 = 0. -/
theorem number_theory_divisibility_mod_compute_final : (1^4 + 1^3 + 1^2 + 1 + 1 : Nat) % 5 = 0 := by
  norm_num

/- Claim c4: Use the geometric-series formula to compute (6^5 - 1) / (6 - 1) and reduce modulo 5 to obtain remainder 0. -/
theorem number_theory_divisibility_geometric_series_mod : (6^4 + 6^3 + 6^2 + 6 + 1 : Nat) % 5 = 0 := by
  norm_num


/- Problem: combinatorics_handshakes
   Topic: combinatorics
   Prompt: In a group of 8 people, every pair shakes hands exactly once. How many handshakes occur?
-/

/- Claim c1: Each handshake corresponds to a unique unordered pair of people. -/
theorem combinatorics_handshakes_handshake_pairs : Nat.choose 8 2 = 28 := by
  native_decide

/- Claim c2: The number of unordered pairs of 8 people is choose(8, 2). -/
theorem combinatorics_handshakes_handshake_choose : Nat.choose 8 2 = 28 := by
  native_decide

/- Claim c3: Compute choose(8, 2) = 28. -/
theorem combinatorics_handshakes_handshake_final : Nat.choose 8 2 = 28 := by
  native_decide


/- Problem: geometry_triangle_angle
   Topic: geometry
   Prompt: In triangle ABC, angles A and B are 50 degrees and 60 degrees respectively. Find angle C.
-/

/- Claim c1: The interior angles of a triangle sum to 180 degrees. -/
theorem geometry_triangle_angle_triangle_angle_sum : (50 + 60 + 70 : Int) = 180 := by
  norm_num

/- Claim c2: Compute angle C = 180 - 50 - 60 = 70. -/
theorem geometry_triangle_angle_triangle_angle_final : (180 - 50 - 60 : Int) = 70 := by
  norm_num

end FormalMathBenchmark.Generated
