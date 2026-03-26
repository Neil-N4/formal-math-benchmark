import Mathlib.Data.Int.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace FormalMathBenchmark

theorem sum_sq_identity (x y : Int) :
    x^2 + y^2 = (x + y)^2 - 2 * x * y := by
  ring

theorem triangle_angles_example :
    180 - 50 - 60 = (70 : Int) := by
  decide

end FormalMathBenchmark
