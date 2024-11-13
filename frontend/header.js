import React, { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can log the error to an error reporting service
    console.log(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children; 
  }
}
```

```javascript
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './Header'; // Assuming Header is in the same directory
import Home from './Home';
import About from './About';
import Services from './Services';
import Contact from './Contact';
import ErrorBoundary from './ErrorBoundary'; // Make sure to import the ErrorBoundary component

const App = () => {
  return (
    <Router>
      <ErrorBoundary>
        <Header />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/about" component={About} />
          <Route path="/services" component={Services} />
          <Route path="/contact" component={Contact} />
          {/* You can add a fallback route here for unmatched paths */}
          <Route render={() => <h1>404: Page Not Found</h1>} />
        </Switch>
      </ErrorBoundary>
    </Router>
  );
};

export default App;