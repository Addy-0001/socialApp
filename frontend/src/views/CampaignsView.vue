<template>
  <main class="flex-1">
    <section class="w-full py-6 md:py-12">
      <div class="container px-4 md:px-6">
        <div class="flex flex-col items-start space-y-4">
          <h1 class="text-3xl font-bold tracking-tighter sm:text-4xl">
            Campaigns
          </h1>
          <p class="max-w-[700px] text-gray-500">
            Discover and support campaigns that are making a difference in the
            world.
          </p>
          <div class="flex flex-col sm:flex-row w-full gap-4">
            <div class="relative flex-1">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
              <input
                type="search"
                placeholder="Search campaigns..."
                class="pl-8 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
              />
            </div>
            <div class="flex gap-2">
              <select
                class="w-[180px] px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-transparent"
              >
                <option value="all">All Categories</option>
                <option value="health">Health</option>
                <option value="environment">Environment</option>
                <option value="education">Education</option>
                <option value="housing">Housing</option>
                <option value="community">Community</option>
                <option value="global">Global Issues</option>
              </select>
              <button
                class="inline-flex h-10 w-10 items-center justify-center rounded-md border border-gray-300 bg-white text-gray-500 hover:bg-gray-50"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div class="mt-6">
          <div
            class="grid w-full grid-cols-3 md:w-auto md:inline-flex border rounded-md overflow-hidden"
          >
            <button
              class="py-2 px-4 text-sm font-medium"
              :class="{
                'bg-green-600 text-white': activeTab === 'all',
                'bg-white text-gray-700 hover:bg-gray-50': activeTab !== 'all',
              }"
              @click="activeTab = 'all'"
            >
              All Campaigns
            </button>
            <button
              class="py-2 px-4 text-sm font-medium"
              :class="{
                'bg-green-600 text-white': activeTab === 'trending',
                'bg-white text-gray-700 hover:bg-gray-50':
                  activeTab !== 'trending',
              }"
              @click="activeTab = 'trending'"
            >
              Trending
            </button>
            <button
              class="py-2 px-4 text-sm font-medium"
              :class="{
                'bg-green-600 text-white': activeTab === 'recent',
                'bg-white text-gray-700 hover:bg-gray-50':
                  activeTab !== 'recent',
              }"
              @click="activeTab = 'recent'"
            >
              Recently Added
            </button>
          </div>
          <div class="mt-6">
            <div
              v-if="activeTab === 'all'"
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              <div
                v-for="campaign in campaigns"
                :key="campaign.id"
                class="overflow-hidden border rounded-lg bg-white"
              >
                <div class="aspect-video relative">
                  <img
                    :src="campaign.image"
                    :alt="campaign.title"
                    class="object-cover w-full h-full"
                  />
                  <span
                    class="absolute top-2 right-2 inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ campaign.category }}
                  </span>
                </div>
                <div class="p-4">
                  <h3 class="text-xl font-bold">{{ campaign.title }}</h3>
                </div>
                <div class="p-4 pt-0 space-y-4">
                  <p class="text-sm text-gray-500">
                    {{ campaign.description }}
                  </p>
                  <div class="space-y-2">
                    <div class="flex justify-between text-sm">
                      <span>${{ campaign.raised }}</span>
                      <span class="text-gray-500">of ${{ campaign.goal }}</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-green-600 h-2 rounded-full"
                        :style="{ width: campaign.progress + '%' }"
                      ></div>
                    </div>
                    <p class="text-xs text-gray-500">
                      {{ campaign.supporters }} supporters
                    </p>
                  </div>
                </div>
                <div class="p-4 pt-0">
                  <router-link :to="`/campaigns/${campaign.id}`" class="w-full">
                    <button
                      class="w-full inline-flex h-10 items-center justify-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-green-700"
                    >
                      Support This Cause
                    </button>
                  </router-link>
                </div>
              </div>
            </div>
            <div
              v-if="activeTab === 'trending'"
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              <div
                v-for="campaign in campaigns.slice(0, 3)"
                :key="campaign.id"
                class="overflow-hidden border rounded-lg bg-white"
              >
                <!-- Same campaign card structure as above -->
                <div class="aspect-video relative">
                  <img
                    :src="campaign.image"
                    :alt="campaign.title"
                    class="object-cover w-full h-full"
                  />
                  <span
                    class="absolute top-2 right-2 inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ campaign.category }}
                  </span>
                </div>
                <div class="p-4">
                  <h3 class="text-xl font-bold">{{ campaign.title }}</h3>
                </div>
                <div class="p-4 pt-0 space-y-4">
                  <p class="text-sm text-gray-500">
                    {{ campaign.description }}
                  </p>
                  <div class="space-y-2">
                    <div class="flex justify-between text-sm">
                      <span>${{ campaign.raised }}</span>
                      <span class="text-gray-500">of ${{ campaign.goal }}</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-green-600 h-2 rounded-full"
                        :style="{ width: campaign.progress + '%' }"
                      ></div>
                    </div>
                    <p class="text-xs text-gray-500">
                      {{ campaign.supporters }} supporters
                    </p>
                  </div>
                </div>
                <div class="p-4 pt-0">
                  <router-link :to="`/campaigns/${campaign.id}`" class="w-full">
                    <button
                      class="w-full inline-flex h-10 items-center justify-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-green-700"
                    >
                      Support This Cause
                    </button>
                  </router-link>
                </div>
              </div>
            </div>
            <div
              v-if="activeTab === 'recent'"
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              <div
                v-for="campaign in campaigns.slice(3, 6)"
                :key="campaign.id"
                class="overflow-hidden border rounded-lg bg-white"
              >
                <!-- Same campaign card structure as above -->
                <div class="aspect-video relative">
                  <img
                    :src="campaign.image"
                    :alt="campaign.title"
                    class="object-cover w-full h-full"
                  />
                  <span
                    class="absolute top-2 right-2 inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ campaign.category }}
                  </span>
                </div>
                <div class="p-4">
                  <h3 class="text-xl font-bold">{{ campaign.title }}</h3>
                </div>
                <div class="p-4 pt-0 space-y-4">
                  <p class="text-sm text-gray-500">
                    {{ campaign.description }}
                  </p>
                  <div class="space-y-2">
                    <div class="flex justify-between text-sm">
                      <span>${{ campaign.raised }}</span>
                      <span class="text-gray-500">of ${{ campaign.goal }}</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-green-600 h-2 rounded-full"
                        :style="{ width: campaign.progress + '%' }"
                      ></div>
                    </div>
                    <p class="text-xs text-gray-500">
                      {{ campaign.supporters }} supporters
                    </p>
                  </div>
                </div>
                <div class="p-4 pt-0">
                  <router-link :to="`/campaigns/${campaign.id}`" class="w-full">
                    <button
                      class="w-full inline-flex h-10 items-center justify-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-green-700"
                    >
                      Support This Cause
                    </button>
                  </router-link>
                </div>
              </div>
            </div>
            <div class="flex justify-center mt-8">
              <button
                class="inline-flex h-10 items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium shadow-sm hover:bg-gray-50"
              >
                Load More
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
  
  <script>
export default {
  name: "Campaigns",
  data() {
    return {
      activeTab: "all",
      campaigns: [
        {
          id: 1,
          title: "Clean Water Initiative",
          description:
            "Providing clean water to communities in need around the world.",
          category: "Environment",
          image: "https://placehold.co/400x200",
          progress: 75,
          supporters: 1243,
          goal: "50,000",
          raised: "37,500",
        },
        {
          id: 2,
          title: "Education for All",
          description:
            "Supporting education programs for underprivileged children.",
          category: "Education",
          image: "https://placehold.co/400x200",
          progress: 45,
          supporters: 876,
          goal: "25,000",
          raised: "11,250",
        },
        {
          id: 3,
          title: "Mental Health Awareness",
          description:
            "Raising awareness about mental health issues and providing support.",
          category: "Health",
          image: "https://placehold.co/400x200",
          progress: 90,
          supporters: 2156,
          goal: "30,000",
          raised: "27,000",
        },
        {
          id: 4,
          title: "Homeless Shelter Support",
          description:
            "Supporting local homeless shelters with resources and volunteers.",
          category: "Housing",
          image: "https://placehold.co/400x200",
          progress: 60,
          supporters: 532,
          goal: "20,000",
          raised: "12,000",
        },
        {
          id: 5,
          title: "Youth Mentorship Program",
          description:
            "Connecting youth with mentors to guide their personal and professional development.",
          category: "Community",
          image: "https://placehold.co/400x200",
          progress: 30,
          supporters: 245,
          goal: "15,000",
          raised: "4,500",
        },
        {
          id: 6,
          title: "Disaster Relief Fund",
          description:
            "Providing immediate assistance to communities affected by natural disasters.",
          category: "Global Issues",
          image: "https://placehold.co/400x200",
          progress: 85,
          supporters: 1876,
          goal: "100,000",
          raised: "85,000",
        },
      ],
    };
  },
};
</script>
  