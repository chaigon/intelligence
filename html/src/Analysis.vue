<template>
    <div style="margin-top:30px;">
      <div style="display:inline-block;width:100%;height:40px;text-align:center;">
        <input class="inquire_ask" v-model="msg" placeholder="IP,域名">
        <button style="height:40px;" @click="inquire()">分析</button>
        <div>
          <button @click="down_work_table">下载</button>
          <button onclick="window.location.href='{% url 'course:down_work_table' %}'">Download</button>
        </div>
      </div>

      <div id="home-leak-pie" style="width:100%;height:850px;display:inline-block;margin-top:30px;"></div>


    </div>
</template>
<style>
  .inquire_ask{
    width: 60%;
    height: 30px;line-height: 30px;
  }
</style>
<script>
  import echarts from 'echarts'
    export default{
      data () {
        return {
          msg: '',
          dataList:[],
          linkList:[],
          work_table_id:1
        }
      },
      methods: {
        ready () {
          this.msg = ''
        },
        inquire () {
          let data = {
            'domain_ip': this.msg,
            'action': 'analysis',
            'user_id': parseInt(window.localStorage.getItem('user_id'))
          }
          this.$http.post('/api/', data).then(function (response) {
            if (response.status === 200) {
              console.log(response. data)
              this.dataList = response. data.data_list
              this.linkList = response.data.link_list
              console.log(this.msg)
//              this.$router.go({name:'Vieualization'})
              this.totalData()
            }
          }, function (response) {

          })
        },
        down_work_table(){
          let data = {
            'work_table_id': this.work_table_id,
            'action': 'down_work_table',
            'user_id': parseInt(window.localStorage.getItem('user_id'))
          }

          this.$http.post('/api/', data).then(function (response) {
            if (response.status === 200) {
              console.log(response. data)
              this.dataList = response. data.data_list
              this.linkList = response.data.link_list
              console.log(this.msg)
//              this.$router.go({name:'Vieualization'})
              this.totalData()
            }
          }, function (response) {

          })
        },
        totalData() {
          let leakPie = echarts.init(document.getElementById("home-leak-pie"));
          let option = {
              title: {
                  text: ''
              },
              tooltip: {},
              animationDurationUpdate: 1500,
              animationEasingUpdate: 'quinticInOut',
              label: {
                  normal: {
                      show: true,
                      textStyle: {
                          fontSize: 12
                      },
                  }
              },
              grid: {
                    top: '30',
                    bottom:'30',
                    left:'30',
                    right:'30',
                    containLabel: true
                  },
              legend: {
                  x: "center",
                  show: false,
                  data: ["朋友", "战友", '亲戚']
              },
              series: [

                  {
                      type: 'graph',
                      layout: 'force',
                      symbolSize: 80,
                      focusNodeAdjacency: true,
                      roam: true,
                      categories: [{
                          name: '朋友',
                          itemStyle: {
                              normal: {
                                  color: "#009800",
                              }
                          }
                      }, {
                          name: '战友',
                          itemStyle: {
                              normal: {
                                  color: "#4592FF",
                              }
                          }
                      }, {
                          name: '亲戚',
                          itemStyle: {
                              normal: {
                                  color: "#3592F",
                              }
                          }
                      }],
                      label: {
                          normal: {
                              show: true,
                              textStyle: {
                                  fontSize: 12
                              },
                          }
                      },
                      force: {
                          repulsion: 1000
                      },
                      edgeSymbolSize: [4, 50],
                      edgeLabel: {
                          normal: {
                              show: true,
                              textStyle: {
                                  fontSize: 10
                              },
                              formatter: "{c}"
                          }
                      },
                      data:this.dataList,
                      links: this.linkList,
                      lineStyle: {
                          normal: {
                              opacity: 0.9,
                              width: 1,
                              curveness: 0
                          }
                      }
                  }
              ]
          };
          leakPie.setOption(option)
        }
      },
      watch: {
      },
      components: {
      }
    }
</script>
