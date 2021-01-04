import { BrowserRouter, Route } from "react-router-dom";
import { Button } from "react-bootstrap";
import Landing from './pages/landing'
import About from './pages/about'

import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <div>
        <Route exact path="/" component={Landing} />
        <Route exact path="/about" component={About} />
      </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
