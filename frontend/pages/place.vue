<template>
  <div
    class="min-h-screen flex flex-col justify-center items-center bg-cyan-900 text-white pt-16"
  >
    <div class="text-center mb-8 max-w-3xl">
      <h1 class="text-5xl font-extrabold">CrossPerks</h1>
      <h2>Serving Portland, OR</h2>
      <p
        class="text-center text-xl text-gray-200 mt-2 font-light leading-relaxed sm:flex sm:gap-2 sm:justify-center h-16 sm:h-fit"
      >
        <span v-if="showTagline" class="block sm:inline text-gray-300">
          Enjoy Exclusive Perks at Local Favorites like
        </span>
        <span class="typing font-bold text-yellow-300 block sm:inline">
          {{ typedText }}
        </span>
      </p>
      <p class="my-12 text-lg text-gray-300 font-medium text-balance">
        Support local businesses. Get rewarded for exploring new spots. Shop as
        usual—earn perks almost every time you checkout.
      </p>
    </div>

    <div
      class="sm:flex sm:flex-row flex flex-col items-center gap-8 p-8 rounded-lg shadow-lg max-w-7xl"
    >
      <NuxtImg
        src="https://images.pexels.com/photos/3907306/pexels-photo-3907306.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2 "
        alt="Perks Illustration"
        class="sm:w-1/2 object-contain mx-auto rounded-lg shadow-lg transition-transform hover:scale-105 duration-1000"
      />
      <div
        class="bg-white p-8 rounded-lg shadow-xl w-full sm:w-1/2 text-gray-800"
      >
        <h2
          class="text-3xl font-extrabold text-center mb-4 text-indigo-700 text-balance"
        >
          Unlock Exclusive Local Perks
        </h2>
        <p class="text-center text-gray-600 mb-6 text-lg text-balance">
          Join our waitlist and be the first to enjoy special offers at your
          favorite local businesses.
        </p>

        <form
          @submit.prevent="submitForm"
          class="space-y-4 flex flex-col items-center"
        >
          <div class="flex flex-col">
            <div class="mb-4">
              <Label class="block text-gray-700 font-semibold mb-2">
                Name</Label
              >
              <Input
                v-model="name"
                type="text"
                placeholder="Enter your name"
                class="input"
                required
              />
            </div>
            <div class="mb-4">
              <Label class="block text-gray-700 font-semibold mb-2"
                >Email</Label
              >
              <Input
                v-model="email"
                type="email"
                placeholder="Enter your email"
                class="input"
                required
              />
            </div>
            <Label class="block text-gray-700 font-semibold mb-2"
              >Favorite Businesses
            </Label>
            <TagsInput v-model="modelValue" class="">
              <TagsInputItem
                v-for="item in modelValue"
                :key="item"
                :value="item"
              >
                <TagsInputItemText />
                <TagsInputItemDelete />
              </TagsInputItem>

              <TagsInputInput
                placeholder="Enter up to 5 businesses you love..."
              />
            </TagsInput>
          </div>
          <Button
            type="submit"
            class="p-6 rounded-[0.75rem] hover:bg-opacity-80"
            >Join the Waitlist
          </Button>
        </form>
        <p
          v-if="successMessage"
          class="text-green-600 text-center mt-4 font-semibold"
        >
          {{ successMessage }}
        </p>
      </div>
    </div>
    <div class="py-16 bg-gray-100 text-gray-900 w-full">
      <!-- Section Title -->
      <div class="max-w-5xl mx-auto text-center">
        <h2 class="text-4xl font-extrabold text-gray-800">
          How CrossPerks Works
        </h2>
        <p class="text-lg text-gray-600 mt-4 text-balance">
          Earn rewards effortlessly while supporting your favorite local
          businesses.
        </p>
      </div>

      <!-- Steps Wrapper -->
      <div
        class="mt-12 flex flex-col lg:flex-row items-center justify-center space-y-12 lg:space-y-0 lg:space-x-16 max-w-6xl mx-auto"
      >
        <!-- Step 1 -->
        <div class="flex flex-col items-center text-center">
          <NuxtImg
            src="https://images.pexels.com/photos/3184183/pexels-photo-3184183.jpeg"
            alt="Visit Local Business"
            class="w-72 h-72 rounded-lg shadow-lg object-cover transition-transform hover:scale-105 duration-1000"
          />
          <p class="mt-4 text-xl font-semibold">Visit Local Businesses</p>
          <p class="w-[90%] sm:w-full text-balance text-gray-600">
            Grab a coffee, hit the gym, or book a spa treatment—just like
            normal.
          </p>
        </div>

        <!-- Hand-Twist Arrow -->
        <!-- <div class="hidden lg:block">
            <svg
              fill="#000000"
              version="1.1"
              id="Capa_1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              width="134px"
              height="134px"
              viewBox="-36.73 -36.73 440.80 440.80"
              xml:space="preserve"
              transform="matrix(1, 0, 0, -1, 0, 0)rotate(45)"
            >
              <g id="SVGRepo_bgCarrier" stroke-width="0">
                <path
                  transform="translate(-36.73, -36.73), scale(13.775000000000002)"
                  d="M16,28.476384289562702C18.00442053968326,28.50806348115101,20.542709193589165,29.768411030800564,21.936761913042847,28.32781313878919C23.568017062893666,26.64209300969054,21.13241380471742,23.069387414583552,22.81448728117942,21.434372265618194C24.872231094242537,19.43419667630651,29.199939961282432,21.610769095618778,31.078715423547557,19.441618397610835C32.57216240249195,17.71735085107316,31.22514100623962,14.833160005451024,30.360253398806115,12.722365871133533C29.542203204370555,10.725880388914826,27.624362442572604,9.489276506390029,26.302180101475717,7.784285521599294C24.961567650190403,6.055528395979677,24.662000718280684,2.612633637960459,22.475122442039154,2.554269703679978C19.72375802306323,2.480840627230992,18.361646675928306,6.095824052063358,16,7.509338457137346C14.91909322551097,8.1562926827019,13.575832709724024,8.06457056282717,12.422429976130202,8.571099297698558C11.240265534655396,9.090259033937787,10.22754929630582,9.838073025815785,9.134053070769781,10.52459003446004C7.6195796464925944,11.475404258255208,5.823433248571514,12.030593024909066,4.698287381746436,13.420457845450805C3.3630304247462193,15.069867691442562,1.4522306431981151,17.155941089297716,2.1407110023804368,19.163292273393864C2.863397456173671,21.27037563373113,6.3371290302466186,20.86108265286056,7.820303852734041,22.523090006588525C9.187619511192011,24.055268577023917,8.492562678822116,26.93313830343284,10.15292632864919,28.141573585894715C11.751387001349098,29.30495503833707,14.02324587576895,28.445142356353223,16,28.476384289562702"
                  fill="#7ed0ec"
                  strokewidth="0"
                ></path>
              </g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g>
              <g id="SVGRepo_iconCarrier">
                <g>
                  <path
                    d="M337.591,0.932c-13.464,6.12-26.315,12.852-39.168,20.196c-11.628,6.12-25.704,12.24-35.496,21.42 c-5.508,4.896,0,15.3,7.344,12.852c0,0,0.612,0,0.612-0.612c1.836,1.224,3.061,2.448,4.896,4.284c0,0.612,0.611,1.836,0.611,2.448 c0.612,1.224,1.836,2.448,3.061,3.672c-17.748,33.048-34.272,66.096-55.08,96.696c-6.12,9.18-12.853,17.748-20.808,25.704 c-19.584-31.212-51.409-67.32-89.965-60.588c-50.796,9.18-23.256,63.647,3.06,82.008c31.212,22.644,58.14,21.42,85.068,0 c12.24,20.808,20.809,44.063,19.584,66.708c-1.836,54.468-50.796,63.647-91.8,49.571c6.12-15.912,7.956-34.271,4.284-50.184 c-6.12-28.764-50.184-54.468-75.888-34.272c-25.092,20.196,22.032,71.604,37.332,82.009c4.284,3.06,9.18,6.119,14.076,8.567 c-0.612,0.612-0.612,1.225-1.224,1.836c-28.152,44.064-65.484,6.12-82.62-25.092c-2.448-4.896-9.18-0.612-7.344,4.284 c14.076,32.436,42.84,70.38,81.396,48.348c9.18-5.508,17.136-13.464,22.644-23.256c33.66,13.464,72.829,13.464,97.308-17.136 c29.376-36.72,11.017-84.456-8.567-119.952c0.611-0.612,0.611-0.612,1.224-1.224c34.884-33.66,56.304-81.396,78.336-124.236 c4.284,3.06,9.181,6.12,13.464,9.18c3.061,1.836,7.345,1.224,9.792-1.224c17.748-20.808,31.212-45.9,35.496-73.44 C351.055,2.768,344.324-2.128,337.591,0.932z M178.471,207.787c-23.256,13.464-46.512-3.06-63.648-18.972 c-22.644-20.808-16.524-54.468,18.36-47.735c17.748,3.672,31.824,19.584,43.452,32.436c6.12,6.732,12.241,14.687,17.749,23.255 C189.488,201.056,183.979,204.728,178.471,207.787z M116.047,319.171C116.047,319.171,115.435,319.171,116.047,319.171 c-16.524-8.567-28.764-20.808-38.556-36.107c-4.284-6.732-7.956-14.076-9.792-22.032c-6.12-20.808,26.928-10.404,35.496-6.12 C126.451,267.764,124.615,297.14,116.047,319.171z M306.379,67.028c-0.612,0-0.612-0.612-1.224-0.612 c0-1.836-1.225-3.672-3.672-4.896c-4.284-1.836-8.568-4.284-12.853-6.732c-1.836-1.224-5.508-4.896-5.508-3.672 c0-0.612-0.612-1.224-1.224-1.224c6.731-3.672,13.464-8.568,20.195-12.24c8.568-4.896,17.748-9.792,26.929-14.688 C324.74,38.264,316.784,53.564,306.379,67.028z"
                  ></path>
                </g>
              </g>
            </svg>
          </div> -->

        <!-- Step 2 -->
        <div class="flex flex-col items-center text-center">
          <NuxtImg
            src="https://images.pexels.com/photos/3183171/pexels-photo-3183171.jpeg"
            alt="Check Out & Unlock Perks"
            class="w-72 h-72 rounded-lg shadow-lg object-cover transition-transform hover:scale-105 duration-1000"
          />
          <p class="mt-4 text-xl font-semibold">Check Out & Unlock Perks</p>
          <p class="text-balance text-gray-600 w-[90%] sm:w-full">
            Scan your CrossPerks QR code at checkout & unlock a surprise perk!
          </p>
        </div>

        <!-- Hand-Twist Arrow -->
        <!-- <div class="hidden lg:block">
            <svg
              fill="#000000"
              version="1.1"
              id="Capa_1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              width="134px"
              height="134px"
              viewBox="-36.73 -36.73 440.80 440.80"
              xml:space="preserve"
              transform="matrix(1, 0, 0, -1, 0, 0)rotate(45)"
            >
              <g id="SVGRepo_bgCarrier" stroke-width="0">
                <path
                  transform="translate(-36.73, -36.73), scale(13.775000000000002)"
                  d="M16,28.476384289562702C18.00442053968326,28.50806348115101,20.542709193589165,29.768411030800564,21.936761913042847,28.32781313878919C23.568017062893666,26.64209300969054,21.13241380471742,23.069387414583552,22.81448728117942,21.434372265618194C24.872231094242537,19.43419667630651,29.199939961282432,21.610769095618778,31.078715423547557,19.441618397610835C32.57216240249195,17.71735085107316,31.22514100623962,14.833160005451024,30.360253398806115,12.722365871133533C29.542203204370555,10.725880388914826,27.624362442572604,9.489276506390029,26.302180101475717,7.784285521599294C24.961567650190403,6.055528395979677,24.662000718280684,2.612633637960459,22.475122442039154,2.554269703679978C19.72375802306323,2.480840627230992,18.361646675928306,6.095824052063358,16,7.509338457137346C14.91909322551097,8.1562926827019,13.575832709724024,8.06457056282717,12.422429976130202,8.571099297698558C11.240265534655396,9.090259033937787,10.22754929630582,9.838073025815785,9.134053070769781,10.52459003446004C7.6195796464925944,11.475404258255208,5.823433248571514,12.030593024909066,4.698287381746436,13.420457845450805C3.3630304247462193,15.069867691442562,1.4522306431981151,17.155941089297716,2.1407110023804368,19.163292273393864C2.863397456173671,21.27037563373113,6.3371290302466186,20.86108265286056,7.820303852734041,22.523090006588525C9.187619511192011,24.055268577023917,8.492562678822116,26.93313830343284,10.15292632864919,28.141573585894715C11.751387001349098,29.30495503833707,14.02324587576895,28.445142356353223,16,28.476384289562702"
                  fill="#7ed0ec"
                  strokewidth="0"
                ></path>
              </g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g>
              <g id="SVGRepo_iconCarrier">
                <g>
                  <path
                    d="M337.591,0.932c-13.464,6.12-26.315,12.852-39.168,20.196c-11.628,6.12-25.704,12.24-35.496,21.42 c-5.508,4.896,0,15.3,7.344,12.852c0,0,0.612,0,0.612-0.612c1.836,1.224,3.061,2.448,4.896,4.284c0,0.612,0.611,1.836,0.611,2.448 c0.612,1.224,1.836,2.448,3.061,3.672c-17.748,33.048-34.272,66.096-55.08,96.696c-6.12,9.18-12.853,17.748-20.808,25.704 c-19.584-31.212-51.409-67.32-89.965-60.588c-50.796,9.18-23.256,63.647,3.06,82.008c31.212,22.644,58.14,21.42,85.068,0 c12.24,20.808,20.809,44.063,19.584,66.708c-1.836,54.468-50.796,63.647-91.8,49.571c6.12-15.912,7.956-34.271,4.284-50.184 c-6.12-28.764-50.184-54.468-75.888-34.272c-25.092,20.196,22.032,71.604,37.332,82.009c4.284,3.06,9.18,6.119,14.076,8.567 c-0.612,0.612-0.612,1.225-1.224,1.836c-28.152,44.064-65.484,6.12-82.62-25.092c-2.448-4.896-9.18-0.612-7.344,4.284 c14.076,32.436,42.84,70.38,81.396,48.348c9.18-5.508,17.136-13.464,22.644-23.256c33.66,13.464,72.829,13.464,97.308-17.136 c29.376-36.72,11.017-84.456-8.567-119.952c0.611-0.612,0.611-0.612,1.224-1.224c34.884-33.66,56.304-81.396,78.336-124.236 c4.284,3.06,9.181,6.12,13.464,9.18c3.061,1.836,7.345,1.224,9.792-1.224c17.748-20.808,31.212-45.9,35.496-73.44 C351.055,2.768,344.324-2.128,337.591,0.932z M178.471,207.787c-23.256,13.464-46.512-3.06-63.648-18.972 c-22.644-20.808-16.524-54.468,18.36-47.735c17.748,3.672,31.824,19.584,43.452,32.436c6.12,6.732,12.241,14.687,17.749,23.255 C189.488,201.056,183.979,204.728,178.471,207.787z M116.047,319.171C116.047,319.171,115.435,319.171,116.047,319.171 c-16.524-8.567-28.764-20.808-38.556-36.107c-4.284-6.732-7.956-14.076-9.792-22.032c-6.12-20.808,26.928-10.404,35.496-6.12 C126.451,267.764,124.615,297.14,116.047,319.171z M306.379,67.028c-0.612,0-0.612-0.612-1.224-0.612 c0-1.836-1.225-3.672-3.672-4.896c-4.284-1.836-8.568-4.284-12.853-6.732c-1.836-1.224-5.508-4.896-5.508-3.672 c0-0.612-0.612-1.224-1.224-1.224c6.731-3.672,13.464-8.568,20.195-12.24c8.568-4.896,17.748-9.792,26.929-14.688 C324.74,38.264,316.784,53.564,306.379,67.028z"
                  ></path>
                </g>
              </g>
            </svg>
          </div> -->

        <!-- Step 3 -->
        <div class="flex flex-col items-center text-center">
          <NuxtImg
            src="https://images.pexels.com/photos/3997997/pexels-photo-3997997.jpeg"
            alt="Redeem Perks"
            class="w-72 h-72 rounded-lg shadow-lg object-cover transition-transform hover:scale-105 duration-1000"
          />
          <p class="mt-4 text-xl font-semibold">
            Redeem Perks at Partner Businesses
          </p>
          <p class="text-balance text-gray-600">
            Use your perk at another awesome local business—keep the cycle
            going!
          </p>
        </div>
      </div>
    </div>
    <div class="h-52 w-full bg-gray-900"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { Check, ChevronsUpDown } from "lucide-vue-next";

import {
  TagsInput,
  TagsInputInput,
  TagsInputItem,
  TagsInputItemDelete,
  TagsInputItemText,
} from "@/components/ui/tags-input";

const modelValue = ref(["Champions Barbershop", "Upper Left Coffeeshop"]);

const frameworks = [
  { value: "next.js", label: "Next.js" },
  { value: "sveltekit", label: "SvelteKit" },
  { value: "nuxt", label: "Nuxt" },
  { value: "remix", label: "Remix" },
  { value: "astro", label: "Astro" },
];

const open = ref(false);
const value = ref("");

const name = ref("");
const email = ref("");
const favoriteBusinesses = ref([]);
const successMessage = ref("");
const showTagline = ref(false);

const businesses = [
  "Joe's Coffee",
  "Zen Gym",
  "Green Spa",
  "Book Haven",
  "and many more businesses",
];
const typedText = ref("");
let isTyping = false;

const typeText = async (text) => {
  if (isTyping) return; // Prevent simultaneous typing animations
  isTyping = true;

  typedText.value = ""; // Reset text before typing
  for (let i = 0; i < text.length; i++) {
    await new Promise((resolve) => setTimeout(resolve, 100)); // Smooth letter-by-letter typing
    typedText.value += text[i];
  }
  isTyping = false;
};

onMounted(() => {
  showTagline.value = true;
  let i = 0;

  const switchText = () => {
    typeText(businesses[i % businesses.length]);
    i++;
  };

  switchText(); // Start immediately
  setInterval(switchText, 4000); // Change every 4 seconds
});
</script>

<style>
.typing {
  display: inline-block;
  overflow: hidden;
  border-right: 3px solid white;
  white-space: nowrap;
  animation: blink 1s step-end infinite;
}
.btn:hover {
  background: #1a1a1a;
  transform: scale(1.02);
  transition: all 0.2s ease-in-out;
}

@keyframes blink {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: white;
  }
}
</style>
