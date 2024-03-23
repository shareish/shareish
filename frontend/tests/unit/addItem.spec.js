import { shallowMount } from "@vue/test-utils";
import TheAddItemView from "@/views/TheAddItemView.vue";
import axios from "axios";

jest.mock('axios');

describe('TheAddItemView.vue', () => {

    it("submit item successfully", async () => {
        const wrapper = shallowMount(TheAddItemView,{
            mocks : {
                $t: () => {}
            },
        });

        await wrapper.setData({
            name: "Test Item",
            description: "This is a test item.",
            type: "DN",
            category1: "Category1",
            category2: "Category2",
            category3: "Category3",
            address_text: "Test Address",
            address_coords: { latitude: 0, longitude: 0 },
            ressource_id: "",
            address: "Test Address",
            use_coordinates: true,
            user_updated_address_field: false,
            startdate: new Date(),
            enddate: new Date(),
            isRecurrent: false,
            visibility: 'PB',
            waitingFormResponse: false,
            geoLocation: null,
            refLocation: null
          });

          axios.post.mockResolvedValueOnce({ data: { id: 'itemId' } });

          await wrapper.vm.submit();

          // Expectations
          expect(wrapper.vm.waitingFormResponse).toBe(false);
    })
})