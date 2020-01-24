public class RestClientStepDefs {

    @Given("^step with table:$")
    public void setUp() throws Throwable {
        resetFields();
    }

    @@Given("^unused step$")
    public void xsetUp() throws Throwable {
        resetFields();
    }

    @@Then("^unused then step$")
    public void Up() throws Throwable {
        resetFields();
    }

    @Given("^using substitution (.*)$")
    public void saveRequest(Scenario result) {
        result.write(getHttpRestLog());
    }

    @Then("^(.*) using substitutions \"([^\"]*)\"$")
    public static void urlEncodingFalse() {
        setUrlEncoding(false);
    }

    @Given("^background (\w+)$")
      public static void urlEncodingFalse() {
        setUrlEncoding(false);
    }

    @When("something to do")
    public static void urlEncodingFalse() {
        setUrlEncoding(false);
    }

    @Then("^I expect a code (\d+)$")
    public static void urlEncodingFalse() {
        setUrlEncoding(false);
    }

}
