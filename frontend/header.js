import React, { createContext, useContext, useState, useEffect } from 'react';

const DataContext = createContext();

export const useData = () => useContext(DataContext);

export const DataProvider = ({ children }) => {
  const [data, setData] = useState({});
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetch and set data from API');
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <DataContext.Provider value={{ data }}>
      {children}
    </DataContext.Provider>
  );
};

import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './Header';
import Home from './Home';
import About from './About';
import Services from './Services';
import Contact from './Contact';
import ErrorBoundary from './ErrorBoundary';
import { DataProvider } from './DataContext';

const App = () => {
  return (
    <Router>
      <DataProvider>
        <ErrorBoundary>
          <Header />
          <Switch>
            <Route path="/" exact component={Home} />
            <Route path="/about" component={About} />
            <Route path="/services" component={Services} />
            <Route path="/contact" component={Contact} />
            <Route render={() => <h1>404: Page Not Found</h1>} />
          </Switch>
        </ErrorBoundary>
      </DataProvider>
    </Router>
  );
};

export default App;