<template>
  <div class="activities__container">
    <div class="topics__header">
      <h2>Study Topics</h2>
    </div>
    <div class="activities__container__inner">
      <div class="topics">
        <ul class="topics__list">
          <li>
            <a href="#" class="active"
              >All
              <span>{{ total_room }}</span>
            </a>
          </li>

          <li v-for="topic in topic_data_set" :key="topic.id">
            <a type="span" href="#">
              {{ topic.name }}<span>{{ topic.total_rooms }}</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
    <div class="scroll-marker">
      <span></span>
    </div>
  </div>
</template>
<script>
import axios from "../axios";
export default {
  name: "TopicComponent",
  data() {
    return {
      total_room: 0,
      topic_data_set: [],
    };
  },

  // Methods are functions that mutate state and trigger updates.
  // They can be bound as event listeners in templates.
  methods: {
    fetchTopic() {
      axios.get("api/topic/").then((response) => {
        // console.log("Network response", response);
        this.topic_data_set = response.data;
        this.total_room = response.data.length;
      });
    },
  },

  // Lifecycle hooks are called at different stages
  // of a component's lifecycle.
  // This function will be called when the component is mounted.
  async mounted() {
    await this.fetchTopic();
  },
};
</script>
<style></style>
