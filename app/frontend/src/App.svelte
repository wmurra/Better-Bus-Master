<script>
  import socket from './utils/socket'
  let number = 1
  socket.on('number', (data)=>{
	number = data
  })
</script>

<div id="main"> 
	<p id="wow">wow</p>
{number}
</div>

<style>
#main {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-size: 250px;
  height: 100%;
  width: 100%; 
  margin: 0;
  background-color: rgb(0, 33, 198);
  color: rgb(0, 102, 255);
  margin: 0px;
  padding: 0px;
}
</style>