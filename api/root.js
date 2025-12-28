export default function handler(req, res) {
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.status(200).send(
`Dev : evil Spy
Created : cause tobi ne bola`
  );
}
