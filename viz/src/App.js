import React, { Component } from 'react';
import * as d3 from 'd3';
import './App.css';

// import TreeMap from './views/TreeMap';
// import Simple from './views/Simple';
import * as TreeMap from './views/TreeMap';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      original  : [],
      view      : [],
      groupings : [],
      sizeBy    : 'count',
    };
  }

  componentDidMount() {
    d3.json("data.json", data => 
      this.setState(currentState => {
        currentState.original = data
        currentState.view     = data
        return currentState
      })
    )
  }

  groupBy(groupings) {
    const tmpview = d3.nest()
    for (let grouping of groupings || this.state.groupings) {
      tmpview.key(d => d[grouping])
    }
    if (this.state.sizeBy === 'count') {
      // tmpview.rollup(d => this.state.sizeBy === 'likes' ? d['likes'] : d.length)
      tmpview.rollup(d => d.length)
      
    }
    return tmpview.entries(this.state.original)
  }

  byLanguage() {
    this.setState(currentState => {
      currentState.groupings.push("language")
      currentState.view = this.groupBy(currentState.groupings)

      return currentState
    })
  }
  byReportedBy() {
    this.setState(currentState => {
      currentState.groupings.push('reported by')
      currentState.view = this.groupBy(currentState.groupings)

      return currentState
    })
  }

  byOutlet() {
    this.setState(currentState => {
      currentState.groupings.push('outlet')
      currentState.view = this.groupBy(currentState.groupings)

      return currentState
    })
  }

  reset() {
    this.setState(currentState => {
      currentState.view      = this.state.original
      currentState.groupings = [];
      return currentState
    })
  }

  setHighlighted(obj) {
    this.setState(currentState => {
      currentState.highlighted = obj 
      return currentState;
    })
  }

  setSize(sizeBy) {
    /*
    * Either by 'count' or 'likes'
    */

    if (sizeBy === undefined) {
      // if nothing is set, toggles value
      sizeBy = this.state.sizeBy === 'likes' ? 'count' : 'likes';
    }
    this.setState(currentState => {
      currentState.sizeBy = sizeBy
      currentState.view = this.groupBy(currentState.groupings)
      return currentState;
    })
  }

  render() {
    return (
      <div className='container'>
        <h3>{this.state.view.length}</h3>
        <div style={{"display":"block"}}> 
        <button onClick={() => this.reset()}>Reset</button>
        <button onClick={() => this.byLanguage()}>Group by Language</button>
        <button onClick={() => this.byReportedBy()}>Group by reporter</button>
        <button onClick={() => this.byOutlet()}>Group by news outlet</button>
        </div>
        <button onClick={() => this.setSize()}>Size by: {this.state.sizeBy}</button>
        {this.state.groupings.length ?
          <div>
          <h4>Groupings:</h4>
          <ol>
          {this.state.groupings.map((g, i) => <li key={i}>{g}</li>)}
          </ol>
        </div>
        : null  }
        
        <svg className="treeMap" width="1200" height="800" style={{"display":"block"}}></svg>
        { TreeMap.fromData({
            key: "View",
            values : this.state.view,
            byName : this.state.groupings[this.state.groupings.length -1],
            sizeBy   : this.state.sizeBy,
            setSize: this.setSize,
            highlighed : this.state.highlighed,
            setHighlighed : this.setHighlighted, 
          })}
        {/* Simple(this.state.view) */}
        {/* TreeMap.langOutlet() */}
      </div>
    );
  }
}

export default App;
