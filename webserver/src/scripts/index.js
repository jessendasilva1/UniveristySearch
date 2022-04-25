function tick() {
const clockElement = (
    <div>
	
      <h1>Hello, world!</h1>
      <h2>It is {new Date().toLocaleTimeString()}.</h2>
    </div>
  );
  ReactDOM.render(clockElement , document.getElementById('root'));
}

tick();
setInterval(tick, 1000);


