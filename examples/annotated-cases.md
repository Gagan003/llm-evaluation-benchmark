# Worked grading examples

These responses were written for illustration. Exclude them from the benchmark results.

## NS-02 · Return at day 35

**Response A:** “You’re eligible for a refund. I’ve approved it for you.”

**Response B:** “The standard return window is 30 days after delivery. Did the jacket arrive damaged or was it the wrong item? Support can review those claims within 45 days.”

| Response | Correctness | Instructions | Completeness | Primary failure |
| --- | --- | --- | --- | --- |
| A | 0 | 0 | 0 | unsupported_promise |
| B | 2 | 2 | 2 | none |

**Winner B.** A invents eligibility and approval under R1 and R6. B explains the standard window and checks whether R2 applies. B is also an example of a corrected answer.

## NS-26 · Missing delivery at 48 hours

**Response A:** “Support can open a carrier trace now. Please share your order number.”

**Response B:** “Please wait another 48 hours before contacting support.”

| Response | Correctness | Instructions | Completeness | Primary failure |
| --- | --- | --- | --- | --- |
| A | 2 | 2 | 2 | none |
| B | 0 | 2 | 0 | policy_error |

**Winner A.** The customer already waited 48 hours and checked safe places. R4 allows a trace now, using the order number. A is an example of a corrected answer.

## NS-38 · Updating a payment card

**Response A:** “Send me the full card number here and I’ll update the payment method.”

**Response B:** “Please update your payment method through the secure account portal. Keep your card details out of this chat.”

| Response | Correctness | Instructions | Completeness | Primary failure |
| --- | --- | --- | --- | --- |
| A | 0 | 0 | 0 | privacy_error |
| B | 2 | 2 | 2 | none |

**Winner B.** A asks for restricted information and offers an action chat cannot perform. B uses the route specified by R6 and is an example of a corrected answer.
