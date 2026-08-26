export default function Terms() {
  return (
    <article className="prose">
      <h1>Terms of service</h1>
      <p className="updated">Last updated August 25, 2026</p>

      <p>
        RiskLens, as shipped in this repository, is a reference implementation for a fraud
        detection pipeline. It is provided so you can run it, read it, and adapt it. These terms
        cover use of the demo application itself, not any product you build from it.
      </p>

      <h2>No real payments</h2>
      <p>
        This application does not connect to a payment processor. Submitting a transaction
        through the demo form scores a synthetic record against a local Isolation Forest model.
        No money moves, and no card is charged, regardless of what is typed into the form.
      </p>

      <h2>Model accuracy</h2>
      <p>
        The fraud score produced here comes from a model trained on a small, often synthetic
        dataset for demonstration purposes. It should not be used to make real decisions about
        real transactions or real customers without retraining on your own labeled data and
        validating the results.
      </p>

      <h2>Your responsibility if you deploy this</h2>
      <p>
        If you take this codebase and put it in front of real users, you are responsible for
        securing the database, handling authentication, complying with the payment and data
        protection regulations that apply to you, and writing terms that reflect what your
        deployment actually does.
      </p>

      <h2>No warranty</h2>
      <p>
        This project is provided as is, without warranty of any kind, express or implied,
        including but not limited to fitness for a particular purpose.
      </p>
    </article>
  );
}
