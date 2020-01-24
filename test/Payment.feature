@SERVICES
Feature: Session-API Account Payment History
  In order to view what I have purchase
  As a client
  I need to be able to view my payment history

  Background:
    Given background 1
    Given background 2


  Scenario Outline: View payment history
    Given step with table:
      | username        | device |
      | movies100months | ios    |
    Given using substitution <response>
    Then I expect a code 200
    Then <response> using substitutions "<code>"

    Examples:
      | response  | code         |
      | json      | SKY6PNFFRDQO |
      | xml       | SKY6PNFFRDQO |
      | xml, json | a            |


  Scenario Outline: View payment history without voucher
    Given using substitution <response>

    Examples:
      | response |
      | json     |
      | xml      |

  @first
  # A comment
  @tag
  Scenario: Simple scenario
    Given background step
    But something to do
