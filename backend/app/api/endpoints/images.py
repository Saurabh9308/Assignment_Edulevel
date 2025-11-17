from fastapi import APIRouter, HTTPException
from app.models.schemas import TopicImagesResponse, ImageMetadata
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.get("/images/{topic_id}", response_model=TopicImagesResponse)
async def get_topic_images(topic_id: str):
    """
    Get all image metadata for a specific topic
    """
    try:
        if not image_service.ensure_topic_images(topic_id):
            raise HTTPException(status_code=404, detail=f"No images available for topic {topic_id}")
        
        images_data = image_service.get_all_images(topic_id)
        
        # Convert to Pydantic models
        images = []
        for img_data in images_data:
            images.append(ImageMetadata(**img_data))
        
        return TopicImagesResponse(
            topic_id=topic_id,
            images=images
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving images: {str(e)}")