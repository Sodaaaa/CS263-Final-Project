import "./App.css";
import React from "react";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import homepage from "./pages/homepage";

// function App() {
//   return (
//     homepage()
//   );
// }

function App() {
  return (
    <BrowserRouter>
      <Route exact path="/" component={homepage} />
      {/* <ul>
            <li><Link to='/'>Home</Link></li>
            <li><Link to='/question'>Post a Question</Link></li>
            <li><Link to='/vote'>Vote</Link></li>
            <li><Link to='/login'>Log in</Link></li>
          </ul> */}
      <Switch>
        <Route path="/homepage" component={homepage} />

      </Switch>
    </BrowserRouter>
  );
}

export default App;
