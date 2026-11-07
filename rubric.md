# Human scoring rubric

Read the prompt, policy, and required checks before scoring. Use the reference answer as an example. Accept any answer that satisfies the checks and policy.

| Score | Correctness | Instruction following | Completeness |
| --- | --- | --- | --- |
| 2 | All material claims agree with the policy and the case facts. | Follows the user's applicable format and scope requirements and respects privacy and authority rules. | Covers all required checks and provides the next step when applicable. |
| 1 | A minor imprecision leaves the decision and next step intact. | A minor format or scope deviation leaves the answer usable. | Misses a secondary detail while giving the customer a usable next step. |
| 0 | A material claim contradicts the policy or invents an outcome. | Misses a central instruction, solicits or repeats sensitive data, or claims an action was completed. | Omits a required detail that changes eligibility or leaves the customer without a usable next step. |

Score each dimension independently. If one defect affects two dimensions, explain both effects in the rationale. User requests that conflict with the policy should be declined or redirected.

## Pairwise preference

Prefer the answer that helps the customer reach the correct outcome. Give priority to material policy, privacy, and authority failures over wording or formatting. Enter `a`, `b`, or `tie` when the two answers are similarly useful. Write one or two sentences that cite a policy clause and point to specific evidence in each response where relevant.

## Failure tags

Assign one primary tag per response with any score below 2. Choose the tag that best explains the most consequential issue. Enter `none` for a response with three scores of 2.

| Tag | Use when |
| --- | --- |
| `policy_error` | An explicit policy claim is wrong, such as the return window. |
| `unsupported_promise` | The answer guarantees an outcome or claims an action occurred without authority. |
| `privacy_error` | The answer asks for or repeats sensitive information. |
| `missed_step` | The answer omits a required detail or practical next step. |
| `instruction_error` | The answer misses a user instruction that the policy allows. |

Review the three examples before starting. If you change the rubric after grading begins, record the change and regrade any affected cases before revealing model identities.
