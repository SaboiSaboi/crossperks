<script setup lang="ts">
import { cn } from "@/lib/utils";
import {
  ProgressIndicator,
  ProgressRoot,
  type ProgressRootProps,
} from "reka-ui";
import { computed, type HTMLAttributes } from "vue";

const props = withDefaults(
  defineProps<ProgressRootProps & { class?: HTMLAttributes["class"] }>(),
  {
    modelValue: 0,
  }
);

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props;

  return delegated;
});
</script>

<template>
  <ProgressRoot
    v-bind="delegatedProps"
    :class="
      cn(
        'relative h-4 w-full overflow-hidden rounded-full bg-primary/20',
        props.class
      )
    "
  >
    <ProgressIndicator
      class="h-full w-full flex-1 bg-indigo-700 transition-all rounded-full"
      :style="`transform: translateX(-${100 - (props.modelValue ?? 0)}%);`"
    />
  </ProgressRoot>
</template>
