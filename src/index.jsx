import React from 'react'
import ReactDOM from 'react-dom'
import styled, { ThemeProvider } from 'styled-components'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";



import Header from './components/Header/Header';
import Planner from './components/Menus/Planner/Planner';
import Editor from './components/Editor/Editor';
import Lander from './components/Lander/Lander';
import Dashboard from './components/Dashboard/Dashboard';

// import Ticker from './components/Ticker/Ticker'
import {darkTheme} from './Theme'

import './index.scss'

const App = function() {
  return (
    <div className="App">
      <ThemeProvider theme={darkTheme}>
      <Router>
      <Switch>
          <Route path="/">
             <Lander/>
          </Route>
          <Route path="/Lander">
             <Planner/>
          </Route>
          <Route path="/Dashboard">
             <Dashboard/>
          </Route>
        </Switch>
      </Router>
      {/* <Header/> */}
     
      {/* <Ticker/> */}
      {/* <Editor/> */}
      </ThemeProvider>
    </div>
  )
}


const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)