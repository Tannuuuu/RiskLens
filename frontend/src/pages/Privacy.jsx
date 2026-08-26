export default function Privacy() {
  return (
    <article className="prose">
      <h1>Privacy policy</h1>
      <p className="updated">Last updated August 25, 2026</p>

      <p>
        This is a demo project. It exists to show how transaction data flows through a fraud
        detection pipeline, not to run a live business. Even so, here is a plain description of
        what the application stores and why, so you can adapt it honestly if you deploy your own
        copy.
      </p>

      <h2>What gets stored</h2>
      <p>
        When you log a transaction through this app, the amount, a card number, a merchant ID,
        an optional category, and an optional location are written to the Postgres database
        alongside the fraud score the model assigns. Alerts store the transaction ID, severity,
        and a short message. No names, emails, or contact details are collected anywhere in this
        project.
      </p>

      <h2>What the card number field is for</h2>
      <p>
        The card number field exists to demonstrate the shape of a real transaction record. Do
        not enter a real card number. The example values in the demo form are placeholders and
        are never validated against a payment network.
      </p>

      <h2>Where data lives</h2>
      <p>
        Everything is stored in the Postgres instance you run, whether that is the local Docker
        container or a database you connect in production. Nothing is sent to a third party by
        this codebase. If you deploy this project publicly, you take on the responsibility of
        securing that database and telling your users what you actually do with their data.
      </p>

      <h2>Retention and deletion</h2>
      <p>
        This template does not include an automated retention policy. Rows persist until you
        delete them directly in the database or truncate the tables defined in{" "}
        <code>database/init.sql</code>.
      </p>

      <h2>Changes</h2>
      <p>
        Since this is a starter project rather than a live product, treat this page as a
        template to rewrite before you use it with real users.
      </p>
    </article>
  );
}
