import React from 'react'
import ReactDOM from 'react-dom'
import styled, { ThemeProvider } from 'styled-components'


import Header from './components/Header/Header'
import Planner from './components/Planner/Planner'
import Editor from './components/Editor/Editor'
// import Ticker from './components/Ticker/Ticker'
import {darkTheme} from './Theme'

import './index.scss'

const App = function() {
  return (
    <div className="App">
      <ThemeProvider theme={darkTheme}>
      <Header/>
      <Planner/>
      {/* <Ticker/> */}
      <Editor/>
      </ThemeProvider>
    </div>
  )
}


const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)